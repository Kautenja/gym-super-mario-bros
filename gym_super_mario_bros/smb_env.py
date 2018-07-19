"""An OpenAI Gym environment for Super Mario Bros. and Lost Levels."""
import os
from nes_py import NESEnv


class SuperMarioBrosEnv(NESEnv):
    """An environment for playing Super Mario Bros with OpenAI Gym."""

    # the custom reward range defined by the environment
    reward_range = (-15, 15)

    # the list of discrete actions
    actions = [
        '',    # NOP
        'L',   # Left
        'R',   # Right
        'LA',  # Left + A
        'LB',  # Left + B
        'LAB', # Left + A + B
        'RA',  # Right + A
        'RB',  # Right + B
        'RAB', # Right + A + B
    ]

    def __init__(self,
        rom_mode=None,
        target_world=None,
        target_level=None,
        lost_levels=False,
    ) -> None:
        """
        Initialize a new Super Mario Bros environment.

        Args:
            rom_mode (str): the ROM mode to use when loading ROMs from disk.
                valid options are:
                -  None: the standard ROM with no modifications
                - 'downsample': down-sampled ROM with static artifacts removed
                - 'pixel': a simpler pixelated version of graphics
                - 'rectangle': an even simpler rectangular version of graphics
            target_world (int): the world to target in the ROM
            target_level (int): the level to target in the given world
            lost_levels (bool): whether to load the ROM with lost levels.
                False will load the original Super Mario Bros. game.
                True will  load the Japanese Super Mario Bros. 2 (commonly
                known as Lost Levels)

        Returns:
            None

        """
        # load the package directory of this class
        package_directory = os.path.dirname(os.path.abspath(__file__))
        # setup the path to the game ROM
        if lost_levels:
            if rom_mode is None:
                rom_name = 'roms/super-mario-bros-2.nes'
            elif rom_mode == 'pixel':
                raise ValueError('pixel_rom not supported for Lost Levels')
            elif rom_mode == 'rectangle':
                raise ValueError('rectangle_rom not supported for Lost Levels')
            elif rom_mode == 'downsample':
                rom_name = 'roms/super-mario-bros-2-downsampled.nes'
            else:
                raise ValueError('invalid rom_mode: {}'.format(repr(rom_mode)))
        else:
            if rom_mode is None:
                rom_name = 'roms/super-mario-bros.nes'
            elif rom_mode == 'pixel':
                rom_name = 'roms/super-mario-bros-pixel.nes'
            elif rom_mode == 'rectangle':
                rom_name = 'roms/super-mario-bros-rect.nes'
            elif rom_mode == 'downsample':
                rom_name = 'roms/super-mario-bros-downsampled.nes'
            else:
                raise ValueError('invalid rom_mode: {}'.format(repr(rom_mode)))
        # convert the path to an absolute path
        self.rom_file_path = os.path.join(package_directory, rom_name)
        super().__init__(self.rom_file_path)

    # MARK: Memory access

    def get_level(self):
        """Return the level of the game."""
        return self.read_mem(0x075f) * 4 + self.read_mem(0x075c)

    def get_world_number(self):
        """Return the current world number (1 to 8)."""
        return self.read_mem(0x075f) + 1

    def get_level_number(self):
        """Return the current level number (1 to 4)."""
        return self.read_mem(0x075c) + 1

    def get_area_number(self):
        """Return the current area number (1 to 5)."""
        return self.read_mem(0x0760) + 1

    def get_score(self):
        """Return the current player score (0 to 999990)."""
        return self.read_mem(0x07de, 6)

    def get_time(self):
        """Return the time left (0 to 999)."""
        return self.read_mem(0x07f8, 3)

    def get_coins(self):
        """Return the number of coins collected (0 to 99)."""
        return self.read_mem(0x07ed, 2)

    def get_life(self):
        """Return the number of remaining lives."""
        return self.read_mem(0x075a)

    def get_x_position(self):
        """Return the current horizontal position."""
        # add the current page 0x6d to the current x
        return self.read_mem(0x6d) * 0x100 + self.read_mem(0x86)

    def get_left_x_position(self):
        """Return the number of pixels from the left of the screen."""
        # subtract the left x position 0x071c from the current x 0x86
        return (self.read_mem(0x86) - self.read_mem(0x071c)) % 256

    def get_y_position(self):
        """Return the current vertical position."""
        return self.read_mem(0x03b8)

    def get_y_viewport(self):
        """
        Return the current y viewport.

        Note:
            1 = in visible viewport
            0 = above viewport
            > 1 below viewport (i.e. dead, falling down a hole)
            up to 5 indicates falling into a hole

        """
        return self.read_mem(0x00b5)

    def get_player_status(self):
        """
        Return the player status.

        Note:
            0 #> small Mario
            1 #> tall Mario
            2+ -> fireball Mario

        """
        return self.read_mem(0x0756)

    def get_player_state(self):
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
        return self.read_mem(0x000e)

    def get_is_dying(self):
        """Return a boolean determining if Mario is in the dying animation."""
        return self.get_player_state() == 0x0b or self.get_y_viewport() > 1

    def get_is_dead(self):
        """Return a boolean determining if Mario is in the dead state."""
        return self.get_player_state() == 0x06

    def get_is_game_over(self):
        """Return 1 if the game has ed or a 0 if it has not."""
        return self.get_life() == 0xff

    def get_is_occupied(self, busy={0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x07}):
        """
        Return boolean whether Mario is occupied by in-game garbage.

        Args:
            busy: the value of states that determine if Mario is busy

        Returns:
            True if Mario's state is in the `busy` set, False otherwise

        """
        return self.get_player_state() in busy






    def get_keys_to_action(self):
        """Return the dictionary of keyboard keys to actions."""
        # Mapping of buttons on the NES joy-pad to keyboard keys
        up =    ord('w')
        down =  ord('s')
        left =  ord('a')
        right = ord('d')
        A =     ord('o')
        B =     ord('p')
        # a list of keyboard keys with indexes matching the discrete actions
        # in self.actions
        keys = [
            (),
            (left, ),
            (right, ),
            tuple(sorted((left, A, ))),
            tuple(sorted((left, B, ))),
            tuple(sorted((left, A, B, ))),
            tuple(sorted((right, A, ))),
            tuple(sorted((right, B, ))),
            tuple(sorted((right, A, B, ))),
        ]
        # A mapping of pressed key combinations to discrete actions in action
        # space
        keys_to_action = {key: index for index, key in enumerate(keys)}

        return keys_to_action


# explicitly define the outward facing API of this module
__all__ = [SuperMarioBrosEnv.__name__]
