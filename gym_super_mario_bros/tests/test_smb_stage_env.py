"""Test cases for the Super Mario Bros stage environment."""
from unittest import TestCase
from ..smb_stage_env import SuperMarioBrosStageEnv


class ShouldStepEnv(TestCase):
    def test(self):
        env = SuperMarioBrosStageEnv(target_world=4, target_stage=2)
        env.reset()
        s, r, d, i = env.step(0)
        self.assertEqual(False, i['flag_get'])
        self.assertEqual(4, i['world'])
        self.assertEqual(2, i['stage'])
        self.assertEqual(400, i['time'])
        self.assertEqual(40, i['x_pos'])
        env.close()
