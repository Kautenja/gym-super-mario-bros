-- MARK: nes_interface

-- global variables
screen = {} -- screen pixels [x,y] = p
pipe_out = nil -- for sending data(output e.g. screen pixels, reward) back to client
pipe_in = nil -- for getting data(input e.g. controller status change) from client

SEP = string.format('%c', 0xFF) -- as separator in communication protocol
IN_SEP = '|'

COMMAND_TABLE = {
    A = "A",
    B = "B",
    U = "up",
    L = "left",
    D = "down",
    R = "right",
    S = "start",
    s = "select"
}

-- exported common functions start with nes_ prefix
-- called before each episode
function nes_reset()
    -- load state so we don't have to instruct to skip title screen
    savestate.load(gamestate)
    x_pos = get_x_position()
    time = get_time()
end


-- called once when emulator starts
function nes_init()
    emu.speedmode("maximum")

    for x = 0, 255 do
        screen[x] = {}
        for y = 0, 223 do
            screen[x][y] = -1
        end
    end

    pipe_prefix = '/tmp/nesgym-pipe'
    -- from emulator to client
    pipe_out, _, _ = io.open(pipe_prefix .. "-in", "w")
    -- from client to emulator
    pipe_in, _, _ = io.open(pipe_prefix .. "-out", "r")

    write_to_pipe("ready" .. SEP .. emu.framecount())
end

-- update_screen - get current screen pixels and store them (256 x 224)
-- Palette is a number from 0 to 127 that represents an RGB color (conversion table in python file)
function nes_update_screen()
    local r, g, b, p
    local framecount = emu.framecount()
    -- NES only has y values in the range 8 to 231, so we need to offset y values by 8
    local offset_y = 8

    write_to_pipe_partial("screen" .. SEP .. framecount .. SEP)
    for y = 0, 223 do
        local screen_string = ""
        for x = 0, 255 do
            r, g, b, p = emu.getscreenpixel(x, y + offset_y, false)
            -- offset p by 20 so the content can never be '\n'
            screen_string = screen_string .. string.format("%c", p+20)
        end
        write_to_pipe_partial(screen_string)
    end
    write_to_pipe_end()
end

function nes_send_data(data)
    write_to_pipe("data" .. SEP .. emu.framecount() .. SEP .. data)
end

function nes_process_command()
    if not pipe_in then
        return false
    end

    local line = pipe_in:read()
    if line ~= nil then
        handle_command(line)
        return true
    end

    return false
end

function nes_ask_for_command()
    write_to_pipe("wait_for_command" .. SEP .. emu.framecount())
end

-- the mapping of commands to pass to the joypad
local joypad_command = {}
local button = nil

--- private functions
-- handle one command
function handle_command(line)
    local body = split(line, IN_SEP)
    local command = body[1]
    if command == 'reset' then
        nes_reset()
    elseif command == 'joypad' then
        -- joypad command
        local buttons = body[2]
        joypad_command = {}
        for i = 1, #buttons do
            local btn = buttons:sub(i,i)
            button = COMMAND_TABLE[buttons:sub(i,i)]
            joypad_command[button] = true
        end
        joypad.set(1, joypad_command)
    end
end

-- write_to_pipe - Write data to pipe
function write_to_pipe(data)
    if data and pipe_out then
        pipe_out:write(data .. SEP .. "\n")
        pipe_out:flush()
    end
end

function write_to_pipe_partial(data)
    if data and pipe_out then
        pipe_out:write(data)
    end
end

function write_to_pipe_end()
    if pipe_out then
        pipe_out:write(SEP .. "\n")
        pipe_out:flush()
    end
end

-- split - Splits a string with a specific delimiter
function split(self, delimiter)
    local results = {}
    local start = 1
    local split_start, split_end    = string.find(self, delimiter, start)
    while split_start do
        table.insert(results, string.sub(self, start, split_start - 1))
        start = split_end + 1
        split_start, split_end = string.find(self, delimiter, start)
    end
    table.insert(results, string.sub(self, start))
    return results
end




-- MARK: Memory reads.

-- readbyterange - Reads a range of bytes and return a number
function readbyterange(address, length)
    local return_value = 0
    for offset = 0,length-1 do
        return_value = return_value * 10
        return_value = return_value + memory.readbyte(address + offset)
    end
    return return_value
end

-- get_level - Returns current level (0-indexed) (0 to 31)
function get_level()
    -- Read the world 0x075f as the base and add the level. there are 4 levels
    -- per world
    return memory.readbyte(0x075f) * 4 + memory.readbyte(0x075c)
end

-- get_world_number - Returns current world number (1 to 8)
function get_world_number()
    return memory.readbyte(0x075f) + 1
end

-- get_level_number - Returns current level number (1 to 4)
function get_level_number()
    return memory.readbyte(0x075c) + 1
end

-- get_area_number - Returns current area number (1 to 5)
function get_area_number()
    return memory.readbyte(0x0760) + 1
end

-- get_coins - Returns the number of coins collected (0 to 99)
function get_coins()
    return tonumber(readbyterange(0x07ed, 2))
end

-- get_life - Returns the number of remaining lives
function get_life()
    return memory.readbyte(0x075a)
end

-- get_score - Returns the current player score (0 to 999990)
function get_score()
    return tonumber(readbyterange(0x07de, 6))
end

-- get_time - Returns the time left (0 to 999)
function get_time()
    return tonumber(readbyterange(0x07f8, 3))
end

-- get_x_position - Returns the current (horizontal) position
function get_x_position()
    -- add the current page 0x6d to the current x
    return memory.readbyte(0x6d) * 0x100 + memory.readbyte(0x86)
end

-- get_left_x_position - Returns number of pixels from left of screen
function get_left_x_position()
    -- subtract the left x position 0x071c from the current x 0x86
    return (memory.readbyte(0x86) - memory.readbyte(0x071c)) % 256
end

-- get_y_position - Returns the current (vertical) position
function get_y_position()
    return memory.readbyte(0x03b8)
end

-- get_y_viewport - Returns the current y viewport
-- 1 = in visible viewport, 0 = above viewport, > 1 below viewport (i.e. dead)
function get_y_viewport()
    return memory.readbyte(0x00b5)
end

-- get_player_status - Returns the player status
-- 0 is small, 1 is big, 2+ is fiery (can shoot fireballs)
function get_player_status()
    return memory.readbyte(0x0756)
end

-- Player State:
-- 0x00 - Leftmost of screen
-- 0x01 - Climbing vine
-- 0x02 - Entering reversed-L pipe
-- 0x03 - Going down a pipe
-- 0x04 - Autowalk
-- 0x05 - Autowalk
-- 0x06 - Player dies
-- 0x07 - Entering area
-- 0x08 - Normal
-- 0x09 - Cannot move
-- 0x0B - Dying
-- 0x0C - Palette cycling, can't move
function get_player_state()
    return memory.readbyte(0x000e)
end

-- Return a boolean determining if Mario is in the dying animation
function is_dying()
    return get_player_state() == 0x0b or get_y_viewport() > 1
end

-- Return a boolean determining if Mario is in the dead state
function is_dead()
    return get_player_state() == 0x06
end

-- Return 1 if the game has ended or a 0 if it has not
function is_game_over()
    return get_life() == 0xff
end

-- MARK: Rewards

-- the current x position of the agent
local x_pos = 0
-- Return the reward for moving forward on the x-axis
function get_x_reward()
    local next_x_pos = get_x_position()
    local _reward = next_x_pos - x_pos
    x_pos = next_x_pos
    return _reward
end

-- the current time step of the in-game clock
local time = 0
-- Return the penalty for staying alive. i.e. the reward stream designed
-- to convince the agent to be fast
function get_time_penalty()
    local next_time = get_time()
    local _reward = next_time - time
    time = next_time
    return _reward
end

-- Return a penalty for
function get_death_penalty()
    if is_dying() or is_dead() then
        return -100
    end
    return 0
end

-- Return the cumulative reward at the current state
function get_reward()
    return get_x_reward() + get_time_penalty() + get_death_penalty()
end

-- MARK: Hacks

-- Force the pre-level timer to 0 to skip the unnecessary frames
function runout_prelevel_timer()
    memory.writebyte(0x07A0, 0)
end

-- Write 6 to the player state register to kill mario.
function kill_mario()
    memory.writebyte(0x000e, 0x06)
end


-- MARK: Main

-- Initialize the NES
nes_init()


-- Press start until the game starts
while get_time() >= time do
    time = get_time()
    -- press and release the start button
    handle_command('joypad|S')
    emu.frameadvance()
    handle_command('joypad|')
    -- force override the timer for pause menus
    runout_prelevel_timer()
    emu.frameadvance()
end


-- Backup the save-state so we don't have to go past pause menu again
gamestate = savestate.object()
savestate.save(gamestate)


-- update screen every screen_update_interval frames
local frame_skip = 4
-- a flag determining if the game is waiting for a reset
local is_waiting_for_reset = false


while true do
    -- skip pre-level stuff if Mario is at starting position
    if get_player_state() == 0 or is_waiting_for_reset then
        runout_prelevel_timer()
    end

    -- If Mario is dying set him to dead to skip the animation
    if is_dying() then
        kill_mario()
        emu.frameadvance()
    end

    -- Check if Mario lost the last life and the state needs reset
    if not is_waiting_for_reset and is_game_over() then
        write_to_pipe("game_over" .. SEP .. emu.framecount())
        is_waiting_for_reset = true
    end

    -- Ignore zero states where the player can't do anything
    if get_player_state() == 0 then
        emu.frameadvance()
    -- check if we're waiting for a reset and dont need to send data
    elseif is_waiting_for_reset then
        is_waiting_for_reset = is_game_over()
        emu.frameadvance()
    -- Check if this cycle should accept a new action as input
    else
        -- Get an action from the pipe
        nes_ask_for_command()
        -- Process the action (i.e press it for one frame)
        local has_command = nes_process_command()
        if not has_command then
            print('pipe closed')
            break
        end
        emu.frameadvance()
        -- get the reward over the frame-skip
        local reward = get_reward()
        for frame_i=1,frame_skip-1 do
            joypad.set(1, joypad_command)
            emu.frameadvance()
            reward = reward + get_reward()
        end
        -- send the reward and the next state to the client
        nes_send_data(string.format("%d", reward))
        nes_update_screen()
    end
end
