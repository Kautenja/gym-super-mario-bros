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
            expected_keys = {
                'character_id',
                'character_status',
                'enemy_defeat_count',
                'health_meter',
                'invulnerability_timer',
                'is_dead',
                'is_dying',
                'is_game_over',
                'item_in_hand_height',
                'level_transition',
                'lives',
                'position_progress',
                'position_progress_max',
                'subspace_visits',
                'x_page',
                'x_screen',
                'y_page',
                'y_screen',
            }
            self.assertTrue(expected_keys <= set(info))
            self.assertEqual('mario', info['character'])
            self.assertEqual(0, info['character_id'])
            self.assertEqual(2, info['character_status'])
            self.assertEqual(0, info['cherries'])
            self.assertEqual(0, info['coins'])
            self.assertEqual(0, info['enemy_defeat_count'])
            self.assertEqual(2, info['health'])
            self.assertEqual(0, info['health_meter'])
            self.assertEqual(0, info['invulnerability_timer'])
            self.assertFalse(info['is_dead'])
            self.assertFalse(info['is_dying'])
            self.assertFalse(info['is_game_over'])
            self.assertEqual(0, info['item_in_hand_height'])
            self.assertEqual(0, info['level'])
            self.assertEqual(False, info['level_complete'])
            self.assertEqual(0, info['level_transition'])
            self.assertEqual(2, info['life'])
            self.assertEqual(3, info['lives'])
            self.assertEqual(0, info['position_progress'])
            self.assertEqual(0, info['position_progress_max'])
            self.assertEqual(1, info['stage'])
            self.assertEqual(0, info['subspace_visits'])
            self.assertEqual(1, info['world'])
            self.assertEqual(0, info['x_page'])
            self.assertEqual(120, info['x_pos'])
            self.assertEqual(120, info['x_screen'])
            self.assertEqual(1, info['y_page'])
            self.assertEqual(448, info['y_pos'])
            self.assertEqual(192, info['y_screen'])
            self.assertFalse(info['clear'])
            self.assertFalse(info['death'])
            self.assertEqual('smb2_usa', info['game'])
            self.assertEqual('smb2_usa', info['game_family'])
            self.assertEqual(0, info['progress'])
            self.assertEqual(0, info['progress_max'])
            self.assertEqual('vanilla', info['rom_mode'])
            self.assertFalse(info['single_stage'])
            self.assertEqual('SuperMarioBros2USA-v0', info['task_id'])
            self.assertFalse(info['timeout'])
            self.assertEqual('1', info['world_label'])
            self.assertIsNone(info['target_world'])
            self.assertIsNone(info['target_stage'])
            self.assertEqual(0.0, info['reward_total_unclipped'])
            self.assertEqual(0.0, info['reward_total_clipped'])
            self.assertEqual(
                {'progress', 'collectibles', 'health', 'completion', 'death'},
                set(info['reward_components']),
            )
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
            self.assertFalse(info['clear'])
            self.assertFalse(info['death'])
            self.assertEqual('smb2_usa', info['game'])
            self.assertTrue(info['single_stage'])
            self.assertEqual('SuperMarioBros2USA-4-2-v0', info['task_id'])
            self.assertEqual(4, info['target_world'])
            self.assertEqual(2, info['target_stage'])
        finally:
            env.close()


class ShouldRewardSuperMarioBros2UsaMovement(TestCase):
    """Test position progress reward behavior."""

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

    def test_vertical_page_wrap_does_not_pollute_progress_max(self):
        env = SuperMarioBros2Env(target=(5, 1), render_mode='rgb_array')
        try:
            env.reset()
            for step in range(96):
                action = 131 if step % 16 in (8, 9, 10, 11) else 130
                _, _, terminated, truncated, info = env.step(action)
                self.assertFalse(terminated)
                self.assertFalse(truncated)

            self.assertLess(info['progress_max'], 1000)
            self.assertLess(info['progress'], 1000)
        finally:
            env.close()

    def test_backtracking_is_not_penalized_by_progress(self):
        env = SuperMarioBros2Env(render_mode='rgb_array')
        try:
            env.reset()
            env.ram[0x0028] = 123
            self.assertEqual(3, env.unwrapped._progress_reward)

            env.ram[0x0028] = 121
            self.assertEqual(0, env.unwrapped._progress_reward)
        finally:
            env.close()

    def test_collectible_health_and_completion_rewards(self):
        env = SuperMarioBros2Env(render_mode='rgb_array')
        try:
            env.reset()

            env.unwrapped._coins_last = 0
            env.unwrapped._cherries_last = 0
            env.ram[0x062a] = 2
            env.ram[0x062b] = 1
            self.assertEqual(9, env.unwrapped._collectible_reward)

            env.unwrapped._health_last = 2
            env.ram[0x04c2] = 0x0f
            self.assertEqual(-5, env.unwrapped._health_reward)

            env.ram[0x04c2] = 0x1f
            self.assertEqual(5, env.unwrapped._health_reward)

            env.ram[0x04ec] = 0x03
            self.assertEqual(50, env.unwrapped._completion_reward)
            self.assertEqual(0, env.unwrapped._completion_reward)
        finally:
            env.close()

    def test_reward_diagnostics_match_clipped_step_reward(self):
        env = SuperMarioBros2Env(render_mode='rgb_array')
        try:
            env.reset()
            env.ram[0x0028] = 123

            reward = env.unwrapped._get_reward()
            info = env.unwrapped._reward_info()

            self.assertEqual(3.0, reward)
            self.assertEqual(3.0, info['reward_components']['progress'])
            self.assertEqual(3.0, info['reward_total_unclipped'])
            self.assertEqual(3.0, info['reward_total_clipped'])
        finally:
            env.close()


class ShouldTerminateSuperMarioBros2UsaEnv(TestCase):
    """Test death, game-over, and level-complete termination helpers."""

    def test_stage_env_terminates_when_life_loss_restarts_another_level(self):
        env = SuperMarioBros2Env(target=(7, 2), render_mode='rgb_array')
        try:
            env.reset()
            terminal_step = None

            for step in range(1, 180):
                _, reward, terminated, truncated, info = env.step(130)
                if terminated or truncated:
                    terminal_step = step, reward, terminated, truncated, info
                    break

            self.assertIsNotNone(terminal_step)
            step, reward, terminated, truncated, info = terminal_step
            self.assertEqual(130, step)
            self.assertEqual(-15, reward)
            self.assertTrue(terminated)
            self.assertFalse(truncated)
            self.assertTrue(info['death'])
            self.assertFalse(info['clear'])
            self.assertEqual(2, info['lives'])
            self.assertEqual(0, info['level'])
            self.assertEqual(1, info['world'])
            self.assertEqual(1, info['stage'])
            self.assertEqual(0.0, info['reward_components']['health'])
            self.assertEqual(-25.0, info['reward_components']['death'])
            self.assertEqual(-25.0, info['reward_total_unclipped'])
            self.assertEqual(-15.0, info['reward_total_clipped'])
        finally:
            env.close()

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
