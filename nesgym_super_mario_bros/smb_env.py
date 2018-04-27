import os
from gym import spaces
from .nesenv import NESEnv


package_directory = os.path.dirname(os.path.abspath(__file__))


class SuperMarioBrosEnv(NESEnv):
    """An environment for playing Super Mario Bros with OpenAI Gym."""

    def __init__(self, **kwargs) -> None:
        """
        Initialize a new Super Mario Bros environment.

        Args:
            kwargs: the key word arguments to pass to the superclass constructor

        Returns:
            None

        """
        super().__init__(**kwargs)
        # setup the paths to the Lua server file and NES ROM.
        self.lua_interface_path = os.path.join(package_directory, 'lua/super-mario.lua')
        self.rom_file_path = os.path.join(package_directory, 'roms/super-mario.nes')
        # setup the discrete action space for the agent
        self.actions = [
            '',
            'U', 'D', 'L', 'R',
            'LA', 'LB', 'LAB',
            'RA', 'RB', 'RAB',
            'A', 'B', 'AB'
        ]
        self.action_space = spaces.Discrete(len(self.actions))


__all__ = [SuperMarioBrosEnv.__name__]
