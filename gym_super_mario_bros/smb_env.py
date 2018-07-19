"""An OpenAI Gym environment for Super Mario Bros. and Lost Levels."""
import os
from nes_py import NESEnv
from ._rom_mode import RomMode


class SuperMarioBrosEnv(NESEnv):
    """An environment for playing Super Mario Bros with OpenAI Gym."""

    def __init__(self,
        rom_mode=RomMode.VANILLA,
        target_world=None,
        target_level=None,
        lost_levels=False,
    ):
        """
        Initialize a new Super Mario Bros environment.

        Args:
            rom_mode (RomMode): the ROM mode to use when loading ROMs from disk
            target_world (int): the world to target in the ROM
            target_level (int): the level to target in the given world
            lost_levels (bool): whether to load the ROM with lost levels.
                - False: load original Super Mario Bros.
                - True: load Super Mario Bros. Lost Levels

        Returns:
            None

        """
        if not isinstance(rom_mode, RomMode):
            raise TypeError('rom_mode must be of type: RomMode')
        self._rom_mode = rom_mode
        # Type and value check the target world parameter
        if target_world is not None and not isinstance(target_world, int):
            raise TypeError('target_world must be of type: int')
        # TODO: value check
        self._target_world = target_world
        # Type and value check the target level parameter
        if target_level is not None and not isinstance(target_level, int):
            raise TypeError('target_level must be of type: int')
        # TODO: value check
        self._target_level = target_level
        # Type and value check the lost levels parameter
        if not isinstance(lost_levels, bool):
            raise TypeError('lost_levels must be of type: bool')
        self._lost_levels = lost_levels
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
        super(SuperMarioBrosEnv, self).__init__(rom)
        # setup a variable to keep track of remaining time locally
        self._time_left = 0
        # setup a variable to keep track of how far into the level Mario is
        self._x_position = 0

    @property
    def rom_mode(self):
        """Return the type of ROM being used."""
        return self._rom_mode

    @property
    def target_world(self):
        """Return world to target for single level mode."""
        return self._target_world

    @property
    def target_level(self):
        """Return the level to target for single level mode."""
        return self._target_level

    @property
    def lost_levels(self):
        """Return True if playing Lost Levels, False otherwise."""
        return self._lost_levels

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
            value *= value
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
            0  -> small Mario
            1  -> tall Mario
            2+ -> fireball Mario

        """
        return self._read_mem(0x0756)

    def _get_player_state(self):
        """
        Return the current player state.

        Note:
            0x00 -> Leftmost of screen
            0x01 -> Climbing vine
            0x02 -> Entering reversed-L pipe
            0x03 -> Going down a pipe
            0x04 -> Auto-walk
            0x05 -> Auto-walk
            0x06 -> Dead
            0x07 -> Entering area
            0x08 -> Normal
            0x09 -> Cannot move
            0x0B -> Dying
            0x0C -> Palette cycling, can't move

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
        while self.get_is_occupied():
            self._runout_prelevel_timer()
            # TODO: use local version of frameadvance (step)
            # TODO: does NESEnv need a simpler step method to access _LIB methods?
            # emu.frameadvance()

    def _kill_mario(self):
        """Skip a death animation by forcing Mario to death."""
        # if there is a specific level specified, ignore the notion of lives
        if self.target_world is not None and self.target_level is not None:
            self._write_mem(0x075a, 0)
        # force Mario's state to dead
        self._write_mem(0x000e, 0x06)

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
            return -15

        return 0

    def _get_reward(self):
        """Return the cumulative reward at the current state."""
        return (
            self._get_x_reward() +
            self._get_time_reward() +
            self._get_death_reward()
        )

    # MARK: Emulation

    def _skip_start_screen(self):
        # Press start until the game starts
        while self._get_time() >= self._time_left:
            self._time_left = self._get_time()
            # TODO: use a proprietary step command instead?
            # press the start button
            self.step(8)
            # release the start button
            self.step(0)
            self._runout_prelevel_timer()
            # TODO: does another step need to occur?
            # emu.frameadvance()






    # def get_keys_to_action(self):
    #     """Return the dictionary of keyboard keys to actions."""
    #     # Mapping of buttons on the NES joy-pad to keyboard keys
    #     up =    ord('w')
    #     down =  ord('s')
    #     left =  ord('a')
    #     right = ord('d')
    #     A =     ord('o')
    #     B =     ord('p')
    #     # a list of keyboard keys with indexes matching the discrete actions
    #     # in self.actions
    #     keys = [
    #         (),
    #         (left, ),
    #         (right, ),
    #         tuple(sorted((left, A, ))),
    #         tuple(sorted((left, B, ))),
    #         tuple(sorted((left, A, B, ))),
    #         tuple(sorted((right, A, ))),
    #         tuple(sorted((right, B, ))),
    #         tuple(sorted((right, A, B, ))),
    #     ]
    #     # A mapping of pressed key combinations to discrete actions in action
    #     # space
    #     keys_to_action = {key: index for index, key in enumerate(keys)}

    #     return keys_to_action


# explicitly define the outward facing API of this module
__all__ = [SuperMarioBrosEnv.__name__]
