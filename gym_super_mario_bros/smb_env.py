"""An OpenAI Gym environment for Super Mario Bros. and Lost Levels."""
import os
from nes_py import NESEnv
from ._rom_mode import RomMode


class SuperMarioBrosEnv(NESEnv):
    """An environment for playing Super Mario Bros with OpenAI Gym."""

    # the legal range of rewards for each step
    reward_range = (-15, 15)

    def __init__(self,
        frameskip=1,
        max_episode_steps=float('inf'),
        rom_mode=RomMode.VANILLA,
        lost_levels=False
    ):
        """
        Initialize a new Super Mario Bros environment.

        Args:
            frameskip (int): the number of frames to skip between steps
            max_episode_steps (float): number of steps before an episode ends
            rom_mode (RomMode): the ROM mode to use when loading ROMs from disk
            lost_levels (bool): whether to load the ROM with lost levels.
                - False: load original Super Mario Bros.
                - True: load Super Mario Bros. Lost Levels

        Returns:
            None

        """
        if not isinstance(rom_mode, RomMode):
            raise TypeError('rom_mode must be of type: RomMode')
        # Type and value check the lost levels parameter
        if not isinstance(lost_levels, bool):
            raise TypeError('lost_levels must be of type: bool')
        # setup the path to the game ROM
        if lost_levels:
            if rom_mode == RomMode.VANILLA:
                rom = 'roms/super-mario-bros-2.nes'
            elif rom_mode == RomMode.PIXEL:
                raise ValueError('pixel_rom not supported for Lost Levels')
            elif rom_mode == RomMode.RECTANGLE:
                raise ValueError('rectangle_rom not supported for Lost Levels')
            elif rom_mode == RomMode.DOWNSAMPLE:
                rom = 'roms/super-mario-bros-2-downsampled.nes'
        else:
            if rom_mode == RomMode.VANILLA:
                rom = 'roms/super-mario-bros.nes'
            elif rom_mode == RomMode.PIXEL:
                rom = 'roms/super-mario-bros-pixel.nes'
            elif rom_mode == RomMode.RECTANGLE:
                rom = 'roms/super-mario-bros-rect.nes'
            elif rom_mode == RomMode.DOWNSAMPLE:
                rom = 'roms/super-mario-bros-downsampled.nes'
        # create an absolute path to the specified ROM
        rom = os.path.join(os.path.dirname(os.path.abspath(__file__)), rom)
        # initialize the super object with the ROM path
        super(SuperMarioBrosEnv, self).__init__(rom,
            frameskip=frameskip,
            max_episode_steps=max_episode_steps,
        )
        # setup a variable to keep track of remaining time locally
        self._time_left = 0
        # setup a variable to keep track of how far into the level Mario is
        self._x_position = 0
        # MARK: Game setup
        # reset the emulator
        self.reset()
        # skip the start screen
        self._skip_start_screen()
        # stall for a frame
        self.step(0)
        # create a backup state to restore from on subsequent calls to reset
        self._backup()

    # MARK: Memory access

    def _read_mem_range(self, address, length):
        """
        Read a range of bytes where each byte is a 10s place figure.

        Args:
            address (int): the address to read from as a 16 bit integer
            length: the number of sequential bytes to read

        Note:
            this method is specific to Mario where three GUI values are stored
            in independent memory slots to save processing time
            - score has 6 10s places
            - coins has 2 10s places
            - time has 3 10s places

        Returns:
            the integer value of this 10s place representation

        """
        value = 0
        # iterate over the length of bytes
        for offset in range(length):
            # shift the value over by 1 10s place
            value *= 10
            # add the next 10s place value
            value += self._read_mem(address + offset)

        return value

    def _get_level(self):
        """Return the level of the game."""
        return self._read_mem(0x075f) * 4 + self._read_mem(0x075c)

    def _get_world_number(self):
        """Return the current world number (1 to 8)."""
        return self._read_mem(0x075f) + 1

    def _get_level_number(self):
        """Return the current level number (1 to 4)."""
        return self._read_mem(0x075c) + 1

    def _get_area_number(self):
        """Return the current area number (1 to 5)."""
        return self._read_mem(0x0760) + 1

    def _get_score(self):
        """Return the current player score (0 to 999990)."""
        # score is represented as a figure with 6 10s places
        return self._read_mem_range(0x07de, 6)

    def _get_time(self):
        """Return the time left (0 to 999)."""
        # time is represented as a figure with 3 10s places
        return self._read_mem_range(0x07f8, 3)

    def _get_coins(self):
        """Return the number of coins collected (0 to 99)."""
        # coins are represented as a figure with 2 10s places
        return self._read_mem_range(0x07ed, 2)

    def _get_life(self):
        """Return the number of remaining lives."""
        return self._read_mem(0x075a)

    def _get_x_position(self):
        """Return the current horizontal position."""
        # add the current page 0x6d to the current x
        return self._read_mem(0x6d) * 0x100 + self._read_mem(0x86)

    def _get_left_x_position(self):
        """Return the number of pixels from the left of the screen."""
        # subtract the left x position 0x071c from the current x 0x86
        return (self._read_mem(0x86) - self._read_mem(0x071c)) % 256

    def _get_y_position(self):
        """Return the current vertical position."""
        return self._read_mem(0x03b8)

    def _get_y_viewport(self):
        """
        Return the current y viewport.

        Note:
            1 = in visible viewport
            0 = above viewport
            > 1 below viewport (i.e. dead, falling down a hole)
            up to 5 indicates falling into a hole

        """
        return self._read_mem(0x00b5)

    def _get_player_status(self):
        """
        Return the player status.

        Note:
            0  : small Mario
            1  : tall Mario
            2+ : fireball Mario

        """
        return self._read_mem(0x0756)

    def _get_player_state(self):
        """
        Return the current player state.

        Note:
            0x00 : Leftmost of screen
            0x01 : Climbing vine
            0x02 : Entering reversed-L pipe
            0x03 : Going down a pipe
            0x04 : Auto-walk
            0x05 : Auto-walk
            0x06 : Dead
            0x07 : Entering area
            0x08 : Normal
            0x09 : Cannot move
            0x0B : Dying
            0x0C : Palette cycling, can't move

        """
        return self._read_mem(0x000e)

    def _get_is_dying(self):
        """Return True if Mario is in dying animation, False otherwise."""
        return self._get_player_state() == 0x0b or self._get_y_viewport() > 1

    def _get_is_dead(self):
        """Return True if Mario is dead, False otherwise."""
        return self._get_player_state() == 0x06

    def _get_is_game_over(self):
        """Return True if the game has ended, False otherwise."""
        return self._get_life() == 0xff

    def _get_is_occupied(self, busy={0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x07}):
        """
        Return boolean whether Mario is occupied by in-game garbage.

        Args:
            busy: the value of states that determine if Mario is busy

        Returns:
            True if Mario's state is in the `busy` set, False otherwise

        """
        return self._get_player_state() in busy

    def _get_is_world_over(self):
        """Return a boolean determining if the world is over."""
        # 0x0770 contains GamePlay mode:
        # 0 => Demo
        # 1 => Standard
        # 2 => End of world
        return self._read_mem(0x0770) == 2

    def _get_is_level_over(self):
        """Return a boolean determining if the level is over."""
        # player float state set to 3 when sliding down flag pole
        return self._read_mem(0x001D) == 3

    # MARK: RAM Hacks

    def _runout_prelevel_timer(self):
        """Force the pre-level timer to 0 to skip frames during a death."""
        self._write_mem(0x07A0, 0)

    def _skip_change_area(self):
        """Skip change area animations by by running down timers."""
        change_area_timer = self._read_mem(0x06DE)
        if change_area_timer > 1 and change_area_timer < 255:
            self._write_mem(0x06DE, 1)

    def _skip_occupied_states(self):
        """Skip occupied states by running out a timer and skipping frames."""
        while self._get_is_occupied() or self._get_is_world_over():
            self._runout_prelevel_timer()
            self._frame_advance(0)

    def _kill_mario(self):
        """Skip a death animation by forcing Mario to death."""
        # force Mario's state to dead
        self._write_mem(0x000e, 0x06)
        # step forward one frame
        self._frame_advance(0)

    def _skip_start_screen(self):
        """Press and release start to skip the start screen."""
        # press and release the start button
        self._frame_advance(8)
        self._frame_advance(0)
        # Press start until the game starts
        while self._get_time() == 0:
            # press and release the start button
            self._frame_advance(8)
            self._frame_advance(0)
            # run-out the prelevel timer to skip the animation
            self._runout_prelevel_timer()
        # after the start screen idle to skip some extra frames
        while self._get_time() >= self._time_left:
            self._time_left = self._get_time()
            self._frame_advance(8)
            self._frame_advance(0)

    # MARK: Reward Calculation

    def _get_x_reward(self):
        """Return the reward based on left right movement between steps."""
        _x_position = self._get_x_position()
        _reward = _x_position - self._x_position
        self._x_position = _x_position
        # resolve an issue where after death the x position resets. The x delta
        # is typically has at most magnitude of 3, 5 is a safe bound
        if _reward < -5 or _reward > 5:
            return 0

        return _reward

    def _get_time_reward(self):
        """Return the reward for the in-game clock ticking."""
        _time_left = self._get_time()
        _reward = _time_left - self._time_left
        self._time_left = _time_left
        # time can only decrease, a positive reward results from a reset and
        # should default to 0 reward
        if _reward > 0:
            return 0

        return _reward

    def _get_death_reward(self):
        """Return the reward earned by dying."""
        if self._get_is_dying() or self._get_is_dead():
            return -25

        return 0

    # MARK: nes-py API calls

    def _will_reset(self):
        """Handle and RAM hacking before a reset occurs."""
        self._time_left = 0
        self._x_position = 0

    def _did_reset(self):
        """Handle any RAM hacking after a reset occurs."""
        self._time_left = self._get_time()
        self._x_position = self._get_x_position()

    def _did_step(self, done):
        """
        Handle any RAM hacking after a step occurs.

        Args:
            done: whether the done flag is set to true

        Returns:
            None

        """
        # if done flag is set a reset is incoming anyway, ignore any hacking
        if done:
            return
        # if mario is dying, then cut to the chase and kill hi,
        if self._get_is_dying():
            self._kill_mario()
        # skip area change (i.e. enter pipe, flag get, etc.)
        self._skip_change_area()
        # skip occupied states like the black screen between lives that shows
        # how many lives the player has left
        self._skip_occupied_states()

    def _get_reward(self):
        """Return the reward after a step occurs."""
        return (
            self._get_x_reward() +
            self._get_time_reward() +
            self._get_death_reward()
        )

    def _get_done(self):
        """Return True if the episode is over, False otherwise."""
        # the life counter will get set to 255 (0xff) when there are no lives
        # left. It goes 2, 1, 0 for the 3 lives of the game
        return self._get_life() == 0xff


# explicitly define the outward facing API of this module
__all__ = [SuperMarioBrosEnv.__name__]
