"""Regression tests for rectangle-mode ROM colors."""
import unittest

import numpy as np

from ..smb_env import SuperMarioBrosEnv


class ShouldDifferentiateRectangleGoombasFromFloor(unittest.TestCase):
    def test(self):
        env = SuperMarioBrosEnv(rom_mode='rectangle', render_mode='rgb_array')
        env.reset()
        obs = None
        for _ in range(120):
            obs, _, terminated, truncated, _ = env.step(0b10000010)
            self.assertFalse(terminated)
            self.assertFalse(truncated)
        env.close()

        goomba_color = np.array([80, 48, 0], dtype=np.uint8)
        floor_color = np.array([228, 92, 16], dtype=np.uint8)
        enemy_region = obs[188:204, 158:174]

        self.assertTrue(np.any(np.all(enemy_region == goomba_color, axis=2)))
        self.assertFalse(np.any(np.all(enemy_region == floor_color, axis=2)))
