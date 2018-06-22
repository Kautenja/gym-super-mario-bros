"""An OpenAI Gym environment for Super Mario Bros. and Lost Levels."""
import os
from gym import spaces
from .nes_env import NESEnv


class SuperMarioBrosEnv(NESEnv):
    """An environment for playing Super Mario Bros with OpenAI Gym."""

    def __init__(self,
        rom_mode: str=None,
        target_world: int=None,
        target_level: int=None,
        lost_levels: bool=False,
        **kwargs
    ) -> None:
        """
        Initialize a new Super Mario Bros environment.

        Args:
            rom_mode: the ROM mode to use when loading ROMs from disk. valid
                options are:
                -  None: the standard ROM with no modifications
                - 'downsample': down-sampled ROM with static artifacts removed
                - 'pixel': a simpler pixelated version of graphics
                - 'rectangle': an even simpler rectangular version of graphics
            target_world: the world to target in the ROM
            target_level: the level to target in the given world
            lost_levels: whether to load the ROM with lost levels. False will
                load the original Super Mario Bros. game. True will load the
                Japanese Super Mario Bros. 2 (commonly known as Lost Levels)
            kwargs: additional keyword arguments for super class constructor

        Returns:
            None

        """
        super().__init__(**kwargs)
        # load the package directory of this class
        package_directory = os.path.dirname(os.path.abspath(__file__))
        # setup the path to the Lua script
        lua_name = 'lua/super-mario-bros.lua'
        self.lua_interface_path = os.path.join(package_directory, lua_name)
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
        # setup the discrete action space for the agent
        self.actions = [
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
        self.action_space = spaces.Discrete(len(self.actions))
        # setup the environment variables for the target levels
        os.environ['lost_levels'] = str(int(lost_levels))
        os.environ['target_world'] = str(target_world)
        os.environ['target_level'] = str(target_level)

    def get_keys_to_action(self) -> dict:
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


__all__ = [SuperMarioBrosEnv.__name__]
