"""Test cases for the Super Mario Bros. 2 (USA) environment."""
from unittest import TestCase

from ..smb2_env import SuperMarioBros2Env
from ..smb2_env import _decode_smb2_level
from ..smb2_env import _decode_smb2_target


class ShouldDecodeSuperMarioBros2UsaTargets(TestCase):
    """Test target validation and linear level mapping."""

    def test_none_target(self):
        self.assertEqual((None, None, None), _decode_smb2_target(None))

    def test_world_stage_targets(self):
        expected = {
            (1, 1): (1, 1, 0),
            (1, 3): (1, 3, 2),
            (2, 1): (2, 1, 3),
            (4, 2): (4, 2, 10),
            (7, 2): (7, 2, 19),
        }
        for target, decoded in expected.items():
            self.assertEqual(decoded, _decode_smb2_target(target))

    def test_level_to_world_stage(self):
        expected = {
            0: (1, 1),
            2: (1, 3),
            3: (2, 1),
            10: (4, 2),
            18: (7, 1),
            19: (7, 2),
        }
        for level, decoded in expected.items():
            self.assertEqual(decoded, _decode_smb2_level(level))

    def test_invalid_target_type(self):
        self.assertRaises(TypeError, _decode_smb2_target, '1-1')

    def test_invalid_world_type(self):
        self.assertRaises(TypeError, _decode_smb2_target, ('1', 1))

    def test_invalid_world_bounds(self):
        self.assertRaises(ValueError, _decode_smb2_target, (0, 1))
        self.assertRaises(ValueError, _decode_smb2_target, (8, 1))

    def test_invalid_stage_type(self):
        self.assertRaises(TypeError, _decode_smb2_target, (1, '1'))

    def test_invalid_stage_bounds(self):
        self.assertRaises(ValueError, _decode_smb2_target, (1, 0))
        self.assertRaises(ValueError, _decode_smb2_target, (1, 4))
        self.assertRaises(ValueError, _decode_smb2_target, (7, 3))


class ShouldStepSuperMarioBros2UsaEnv(TestCase):
    """Test vanilla reset, step, render, and info behavior."""

    def test(self):
        env = SuperMarioBros2Env(render_mode='rgb_array')
        try:
            self.assertFalse(env.unwrapped.is_single_stage_env)
            self.assertIsNone(env.unwrapped._target_world)
            self.assertIsNone(env.unwrapped._target_stage)
            self.assertIsNone(env.unwrapped._target_level)

            reset_result = env.reset()
            self.assertEqual(2, len(reset_result))
            state, reset_info = reset_result
            self.assertEqual(env.observation_space.shape, state.shape)
            self.assertIsInstance(reset_info, dict)

            step_result = env.step(0)
            self.assertEqual(5, len(step_result))
            state, reward, terminated, truncated, info = step_result
            self.assertEqual(env.observation_space.shape, state.shape)
            self.assertEqual(0.0, reward)
            self.assertIsInstance(terminated, bool)
            self.assertIsInstance(truncated, bool)
            self.assertFalse(terminated)
            self.assertFalse(truncated)
            self.assertIsNotNone(env.render())
            self.assertEqual('mario', info['character'])
            self.assertEqual(0, info['cherries'])
            self.assertEqual(0, info['coins'])
            self.assertEqual(2, info['health'])
            self.assertEqual(0, info['level'])
            self.assertEqual(False, info['level_complete'])
            self.assertEqual(2, info['life'])
            self.assertEqual(1, info['stage'])
            self.assertEqual(1, info['world'])
            self.assertEqual(120, info['x_pos'])
            self.assertEqual(448, info['y_pos'])
        finally:
            env.close()


class ShouldStepSuperMarioBros2UsaStageEnv(TestCase):
    """Test single-stage target reset, step, render, and info behavior."""

    def test(self):
        env = SuperMarioBros2Env(target=(4, 2), render_mode='rgb_array')
        try:
            self.assertTrue(env.unwrapped.is_single_stage_env)
            self.assertEqual(4, env.unwrapped._target_world)
            self.assertEqual(2, env.unwrapped._target_stage)
            self.assertEqual(10, env.unwrapped._target_level)

            state, reset_info = env.reset()
            self.assertEqual(env.observation_space.shape, state.shape)
            self.assertIsInstance(reset_info, dict)

            state, reward, terminated, truncated, info = env.step(0)
            self.assertEqual(env.observation_space.shape, state.shape)
            self.assertEqual(0.0, reward)
            self.assertFalse(terminated)
            self.assertFalse(truncated)
            self.assertIsNotNone(env.render())
            self.assertEqual(10, info['level'])
            self.assertEqual(4, info['world'])
            self.assertEqual(2, info['stage'])
            self.assertEqual(120, info['x_pos'])
            self.assertEqual(128, info['y_pos'])
        finally:
            env.close()


class ShouldRewardSuperMarioBros2UsaMovement(TestCase):
    """Test horizontal movement reward behavior."""

    def test(self):
        env = SuperMarioBros2Env(render_mode='rgb_array')
        try:
            env.reset()
            rewards = []
            for _ in range(20):
                _, reward, _, _, _ = env.step(128)
                rewards.append(reward)

            self.assertGreater(sum(rewards), 0)
            self.assertTrue(any(reward > 0 for reward in rewards))
        finally:
            env.close()


class ShouldTerminateSuperMarioBros2UsaEnv(TestCase):
    """Test death, game-over, and level-complete termination helpers."""

    def test_stage_env_terminates_on_death_and_completion(self):
        env = SuperMarioBros2Env(target=(1, 1), render_mode='rgb_array')
        try:
            env.reset()
            env.ram[0x04ec] = 0x01
            self.assertTrue(env.unwrapped._get_terminated())
            self.assertEqual(-25, env.unwrapped._death_penalty)

            env.ram[0x04ec] = 0x03
            self.assertTrue(env.unwrapped._get_terminated())
            self.assertTrue(env.unwrapped._get_info()['level_complete'])
        finally:
            env.close()

    def test_full_env_terminates_on_game_over(self):
        env = SuperMarioBros2Env(render_mode='rgb_array')
        try:
            env.reset()
            env.ram[0x04ec] = 0x01
            self.assertFalse(env.unwrapped._get_terminated())

            env.ram[0x04ec] = 0x02
            self.assertTrue(env.unwrapped._get_terminated())
        finally:
            env.close()
