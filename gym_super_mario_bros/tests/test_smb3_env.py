"""Test cases for the Super Mario Bros. 3 environment."""
from unittest import TestCase

from ..smb3_env import SuperMarioBros3Env
from ..smb3_env import _decode_smb3_target


class ShouldDecodeSuperMarioBros3Targets(TestCase):
    """Test target validation for the validated SMB3 entry point."""

    def test_none_target(self):
        self.assertEqual((None, None), _decode_smb3_target(None))

    def test_world_1_stage_1_target(self):
        self.assertEqual((1, 1), _decode_smb3_target((1, 1)))

    def test_invalid_target_type(self):
        self.assertRaises(TypeError, _decode_smb3_target, '1-1')

    def test_invalid_world_type(self):
        self.assertRaises(TypeError, _decode_smb3_target, ('1', 1))

    def test_invalid_world_bounds(self):
        self.assertRaises(ValueError, _decode_smb3_target, (0, 1))
        self.assertRaises(ValueError, _decode_smb3_target, (2, 1))

    def test_invalid_stage_type(self):
        self.assertRaises(TypeError, _decode_smb3_target, (1, '1'))

    def test_invalid_stage_bounds(self):
        self.assertRaises(ValueError, _decode_smb3_target, (1, 0))
        self.assertRaises(ValueError, _decode_smb3_target, (1, 2))


class ShouldStepSuperMarioBros3Env(TestCase):
    """Test vanilla reset, step, render, and info behavior."""

    def test(self):
        env = SuperMarioBros3Env(render_mode='rgb_array')
        try:
            self.assertFalse(env.unwrapped.is_single_stage_env)
            self.assertIsNone(env.unwrapped._target_world)
            self.assertIsNone(env.unwrapped._target_stage)

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
            expected_keys = {
                'card_selection',
                'flight_timer',
                'invulnerability_timer',
                'is_dying',
                'is_game_over',
                'lives',
                'p_meter_full',
                'p_meter_timer',
                'pipe_timer',
                'powerup_level',
                'star_timer',
                'status_value',
                'x_page',
                'x_pos_max',
                'x_screen',
                'y_page',
                'y_screen',
            }
            self.assertTrue(expected_keys <= set(info))
            self.assertEqual(0, info['card_selection'])
            self.assertFalse(info['flag_get'])
            self.assertEqual(0, info['flight_timer'])
            self.assertTrue(info['in_level'])
            self.assertEqual(0, info['invulnerability_timer'])
            self.assertFalse(info['is_dying'])
            self.assertFalse(info['is_game_over'])
            self.assertEqual(4, info['life'])
            self.assertEqual(4, info['lives'])
            self.assertEqual(0, info['map_x'])
            self.assertEqual(0, info['map_y'])
            self.assertEqual(0, info['p_meter'])
            self.assertFalse(info['p_meter_full'])
            self.assertEqual(0, info['p_meter_timer'])
            self.assertEqual(0, info['pipe_timer'])
            self.assertEqual(0, info['powerup_level'])
            self.assertEqual(0, info['score'])
            self.assertEqual(1, info['stage'])
            self.assertEqual(0, info['star_timer'])
            self.assertEqual('small', info['status'])
            self.assertEqual(0, info['status_value'])
            self.assertEqual(297, info['time'])
            self.assertEqual(1, info['world'])
            self.assertEqual(0, info['x_page'])
            self.assertEqual(24, info['x_pos'])
            self.assertEqual(24, info['x_pos_max'])
            self.assertEqual(24, info['x_screen'])
            self.assertEqual(1, info['y_page'])
            self.assertEqual(384, info['y_pos'])
            self.assertEqual(128, info['y_screen'])
        finally:
            env.close()


class ShouldStepSuperMarioBros3StageEnv(TestCase):
    """Test single-stage target reset, step, render, and info behavior."""

    def test(self):
        env = SuperMarioBros3Env(target=(1, 1), render_mode='rgb_array')
        try:
            self.assertTrue(env.unwrapped.is_single_stage_env)
            self.assertEqual(1, env.unwrapped._target_world)
            self.assertEqual(1, env.unwrapped._target_stage)

            state, reset_info = env.reset()
            self.assertEqual(env.observation_space.shape, state.shape)
            self.assertIsInstance(reset_info, dict)

            state, reward, terminated, truncated, info = env.step(0)
            self.assertEqual(env.observation_space.shape, state.shape)
            self.assertEqual(0.0, reward)
            self.assertFalse(terminated)
            self.assertFalse(truncated)
            self.assertIsNotNone(env.render())
            self.assertFalse(info['flag_get'])
            self.assertTrue(info['in_level'])
            self.assertEqual(4, info['life'])
            self.assertEqual(1, info['world'])
            self.assertEqual(1, info['stage'])
            self.assertEqual(24, info['x_pos'])
            self.assertEqual(384, info['y_pos'])
        finally:
            env.close()


class ShouldRewardSuperMarioBros3Movement(TestCase):
    """Test position progress reward behavior."""

    def test(self):
        env = SuperMarioBros3Env(render_mode='rgb_array')
        try:
            env.reset()
            rewards = []
            x_positions = []
            for _ in range(60):
                _, reward, terminated, truncated, info = env.step(128)
                rewards.append(reward)
                x_positions.append(info['x_pos'])
                self.assertFalse(terminated)
                self.assertFalse(truncated)

            self.assertGreater(sum(rewards), 0)
            self.assertGreater(max(x_positions), 24)
            self.assertTrue(any(reward > 0 for reward in rewards))
        finally:
            env.close()

    def test_backtracking_is_not_penalized_by_progress(self):
        env = SuperMarioBros3Env(render_mode='rgb_array')
        try:
            env.reset()
            env.ram[0x0090] = 27
            self.assertEqual(3, env.unwrapped._progress_reward)

            env.ram[0x0090] = 25
            self.assertEqual(0, env.unwrapped._progress_reward)
        finally:
            env.close()

    def test_score_powerup_and_completion_rewards(self):
        env = SuperMarioBros3Env(render_mode='rgb_array')
        try:
            env.reset()

            env.unwrapped._score_last = 0
            env.ram[0x0715:0x0718] = [0, 0, 10]
            self.assertEqual(1, env.unwrapped._score_reward)

            env.unwrapped._status_last = 0
            env.ram[0x00ed] = 1
            self.assertEqual(5, env.unwrapped._powerup_reward)

            env.unwrapped._entered_level = True
            env.unwrapped._life_start = 4
            env.ram[0x0736] = 4
            env.ram[0x05ee] = 0
            env.ram[0x05ef] = 0
            env.ram[0x05f0] = 0
            env.ram[0x0075] = 0x20
            env.ram[0x0079] = 0x40
            self.assertEqual(50, env.unwrapped._completion_reward)
            self.assertEqual(0, env.unwrapped._completion_reward)
        finally:
            env.close()


class ShouldTerminateSuperMarioBros3Env(TestCase):
    """Test stage-return, death, and game-over termination helpers."""

    def test_stage_env_terminates_on_death_and_completion(self):
        env = SuperMarioBros3Env(target=(1, 1), render_mode='rgb_array')
        try:
            env.reset()
            env.unwrapped._life_start = 4
            env.ram[0x0736] = 3

            self.assertTrue(env.unwrapped._get_terminated())
            self.assertEqual(-25, env.unwrapped._death_penalty)

            env.unwrapped._life_start = 4
            env.unwrapped._life_last = 4
            env.ram[0x0736] = 4
            env.ram[0x05ee] = 0
            env.ram[0x05ef] = 0
            env.ram[0x05f0] = 0
            env.ram[0x0075] = 0x20
            env.ram[0x0079] = 0x40

            self.assertTrue(env.unwrapped._get_terminated())
            self.assertTrue(env.unwrapped._get_info()['flag_get'])
        finally:
            env.close()

    def test_full_env_terminates_on_game_over_only(self):
        env = SuperMarioBros3Env(render_mode='rgb_array')
        try:
            env.reset()
            env.unwrapped._life_start = 4
            env.ram[0x0736] = 3

            self.assertFalse(env.unwrapped._get_terminated())

            env.ram[0x0736] = 0xff
            self.assertTrue(env.unwrapped._get_terminated())
        finally:
            env.close()
