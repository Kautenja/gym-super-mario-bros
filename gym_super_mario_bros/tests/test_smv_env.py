"""Test cases for the Super Mario Bros meta environment."""
from unittest import TestCase
from ..smb_env import SuperMarioBrosEnv


class ShouldStepEnv(TestCase):
    def test(self):
        env = SuperMarioBrosEnv()
        env.reset()
        s, r, d, i = env.step(0)
        self.assertEqual(0, i['coins'])
        self.assertEqual(False, i['flag_get'])
        self.assertEqual(3, i['life'])
        self.assertEqual(1, i['world'])
        self.assertEqual(0, i['score'])
        self.assertEqual(1, i['stage'])
        self.assertEqual(400, i['time'])
        self.assertEqual(40, i['x_pos'])
        env.close()
