import os
from gym import spaces
from .nes_env import NESEnv


class SuperMarioBrosEnv(NESEnv):
    """An environment for playing Super Mario Bros with OpenAI Gym."""

    def __init__(self, downsampled_rom: bool=False, **kwargs) -> None:
        """
        Initialize a new Super Mario Bros environment.

        Args:
            downsampled_rom: whether to use the downsampled ROM

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
        if downsampled_rom:
            rom_name = 'roms/super-mario-bros-downsampled.nes'
        else:
            rom_name = 'roms/super-mario-bros.nes'
        self.rom_file_path = os.path.join(package_directory, rom_name)
        # setup the discrete action space for the agent
        self.actions = [
            '',    # NOP
            'U',   # Up
            'D',   # Down
            'L',   # Left
            'R',   # Right
            'LA',  # Left + A
            'LB',  # Left + B
            'LAB', # Left + A + B
            'RA',  # Right + A
            'RB',  # Right + B
            'RAB', # Right + A + B
            'A',   # A
            'B',   # B
            'AB'   # A + B
        ]
        self.action_space = spaces.Discrete(len(self.actions))


__all__ = [SuperMarioBrosEnv.__name__]
