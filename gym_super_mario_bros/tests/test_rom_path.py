"""Test cases for packaged ROM paths."""
import os
from unittest import TestCase

from .._roms import rom_path
from .._roms import smb2_rom_path
from .._roms import smb3_rom_path
from ..smb2_env import SuperMarioBros2Env
from ..smb3_env import SuperMarioBros3Env
from ..smb_env import SuperMarioBrosEnv


_LOST_LEVELS_ROM_FILES = {
    'vanilla': 'super-mario-bros-lost-levels.nes',
    'downsample': 'super-mario-bros-lost-levels-downsample.nes',
}


class ShouldResolveLostLevelsRomPaths(TestCase):
    """Test that Lost Levels ROM modes point at the renamed packaged files."""

    def test(self):
        for rom_mode, filename in _LOST_LEVELS_ROM_FILES.items():
            path = rom_path(True, rom_mode)

            self.assertEqual(filename, os.path.basename(path))
            self.assertTrue(os.path.isfile(path))


class ShouldLoadLostLevelsRomFiles(TestCase):
    """Test that the renamed Lost Levels ROM files load into the NES env."""

    def test(self):
        for rom_mode in _LOST_LEVELS_ROM_FILES:
            env = SuperMarioBrosEnv(
                lost_levels=True,
                rom_mode=rom_mode,
                render_mode='rgb_array',
            )
            try:
                state, info = env.reset()

                self.assertEqual(env.observation_space.shape, state.shape)
                self.assertIsInstance(info, dict)
            finally:
                env.close()


class ShouldResolveSuperMarioBros2UsaRomPath(TestCase):
    """Test that Super Mario Bros. 2 (USA) points at the packaged ROM."""

    def test(self):
        path = smb2_rom_path()

        self.assertEqual('super-mario-bros-2.nes', os.path.basename(path))
        self.assertTrue(os.path.isfile(path))


class ShouldLoadSuperMarioBros2UsaRomFile(TestCase):
    """Test that the Super Mario Bros. 2 (USA) ROM loads into the NES env."""

    def test(self):
        env = SuperMarioBros2Env(render_mode='rgb_array')
        try:
            state, info = env.reset()

            self.assertEqual(env.observation_space.shape, state.shape)
            self.assertIsInstance(info, dict)
        finally:
            env.close()


class ShouldResolveSuperMarioBros3RomPath(TestCase):
    """Test that Super Mario Bros. 3 points at the packaged ROM."""

    def test(self):
        path = smb3_rom_path()

        self.assertEqual('super-mario-bros-3.nes', os.path.basename(path))
        self.assertTrue(os.path.isfile(path))


class ShouldLoadSuperMarioBros3RomFile(TestCase):
    """Test that the Super Mario Bros. 3 ROM loads into the NES env."""

    def test(self):
        env = SuperMarioBros3Env(render_mode='rgb_array')
        try:
            state, info = env.reset()

            self.assertEqual(env.observation_space.shape, state.shape)
            self.assertIsInstance(info, dict)
        finally:
            env.close()
