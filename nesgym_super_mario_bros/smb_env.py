import os
from gym import spaces
from .nesenv import NESEnv


package_directory = os.path.dirname(os.path.abspath(__file__))


class SuperMarioBrosEnv(NESEnv):
    def __init__(self):
        super().__init__()
        self.lua_interface_path = os.path.join(package_directory, 'lua/super-mario.lua')
        self.rom_file_path = os.path.join(package_directory, 'roms/super-mario.nes')
        self.actions = [
            '',
            'U', 'D', 'L', 'R',
            'LA', 'LB', 'LAB',
            'RA', 'RB', 'RAB',
            'A', 'B', 'AB'
        ]
        self.action_space = spaces.Discrete(len(self.actions))


__all__ = [SuperMarioBrosEnv.__name__]
