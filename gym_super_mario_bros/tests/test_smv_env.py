"""Test cases for the Super Mario Bros meta environment."""
from unittest import TestCase
from ..smb_env import SuperMarioBrosEnv


class ShouldRaiseErrorOnInvalidRomMode(TestCase):
    def test(self):
        self.assertRaises(ValueError, SuperMarioBrosEnv, rom_mode=-1)
        self.assertRaises(ValueError, SuperMarioBrosEnv, rom_mode=5)
        self.assertRaises(ValueError, SuperMarioBrosEnv, rom_mode=-1, lost_levels=True)
        self.assertRaises(ValueError, SuperMarioBrosEnv, rom_mode=5, lost_levels=True)


class ShouldRaiseErrorOnInvalidTypeLostLevels(TestCase):
    def test(self):
        self.assertRaises(TypeError, SuperMarioBrosEnv, lost_levels='foo')


class ShouldRaiseErrorOnInvalidTypeWorld(TestCase):
    def test(self):
        self.assertRaises(TypeError, SuperMarioBrosEnv, target=('foo', 1))


class ShouldRaiseErrorOnBelowBoundsWorld(TestCase):
    def test(self):
        self.assertRaises(ValueError, SuperMarioBrosEnv, target=(0, 1))
        self.assertRaises(ValueError, SuperMarioBrosEnv, target=(0, 1), lost_levels=True)


class ShouldRaiseErrorOnAboveBoundsWorld(TestCase):
    def test(self):
        self.assertRaises(ValueError, SuperMarioBrosEnv, target=(9, 1))
        self.assertRaises(ValueError, SuperMarioBrosEnv, target=(13, 1), lost_levels=True)


class ShouldRaiseErrorOnInvalidTypeStage(TestCase):
    def test(self):
        self.assertRaises(TypeError, SuperMarioBrosEnv, target=('foo', 1))


class ShouldRaiseErrorOnBelowBoundsStage(TestCase):
    def test(self):
        self.assertRaises(ValueError, SuperMarioBrosEnv, target=(1, 0))
        self.assertRaises(ValueError, SuperMarioBrosEnv, target=(1, 0), lost_levels=True)


class ShouldRaiseErrorOnAboveBoundsStage(TestCase):
    def test(self):
        self.assertRaises(ValueError, SuperMarioBrosEnv, target=(1, 5))
        self.assertRaises(ValueError, SuperMarioBrosEnv, target=(1, 5), lost_levels=True)


class ShouldStepGameEnv(TestCase):
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


class ShouldStepStageEnv(TestCase):
    def test(self):
        env = SuperMarioBrosEnv(target=(4, 2))
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
