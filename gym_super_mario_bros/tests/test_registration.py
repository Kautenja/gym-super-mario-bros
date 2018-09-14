"""Test cases for the gym registered environments."""
from unittest import TestCase
from .._registration import make


class ShouldMakeSuperMarioBros_v0(TestCase):
    def test(self):
        env = make('SuperMarioBros-v0')
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

class ShouldMakeSuperMarioBros_4_2_v0(TestCase):
    def test(self):
        env = make('SuperMarioBros-4-2-v0')
        env.reset()
        s, r, d, i = env.step(0)
        self.assertEqual(0, i['coins'])
        self.assertEqual(False, i['flag_get'])
        self.assertEqual(3, i['life'])
        self.assertEqual(4, i['world'])
        self.assertEqual(0, i['score'])
        self.assertEqual(2, i['stage'])
        self.assertEqual(400, i['time'])
        self.assertEqual(40, i['x_pos'])
        env.close()
