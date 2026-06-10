"""Test cases for the Super Mario Bros. 3 environment."""
from unittest import TestCase

from ..smb3_env import SuperMarioBros3Env
from ..smb3_env import _decode_smb3_target


class ShouldDecodeSuperMarioBros3Targets(TestCase):
    """Test target validation for the validated SMB3 entry points."""

    def test_none_target(self):
        self.assertEqual((None, None), _decode_smb3_target(None))

    def test_world_1_stage_1_target(self):
        self.assertEqual((1, 1), _decode_smb3_target((1, 1)))

    def test_validated_world_1_targets(self):
        for stage in (2, 4, 6):
            self.assertEqual((1, stage), _decode_smb3_target((1, stage)))

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
        self.assertRaises(ValueError, _decode_smb3_target, (1, 3))
        self.assertRaises(ValueError, _decode_smb3_target, (1, 5))
        self.assertRaises(ValueError, _decode_smb3_target, (1, 7))


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
            self.assertFalse(info['clear'])
            self.assertFalse(info['death'])
            self.assertEqual('smb3', info['game'])
            self.assertEqual('smb3', info['game_family'])
            self.assertEqual(24, info['progress'])
            self.assertEqual(24, info['progress_max'])
            self.assertEqual('vanilla', info['rom_mode'])
            self.assertFalse(info['single_stage'])
            self.assertEqual('SuperMarioBros3-v0', info['task_id'])
            self.assertFalse(info['timeout'])
            self.assertEqual('1', info['world_label'])
            self.assertIsNone(info['target_world'])
            self.assertIsNone(info['target_stage'])
            self.assertEqual(0.0, info['reward_total_unclipped'])
            self.assertEqual(0.0, info['reward_total_clipped'])
            self.assertEqual(
                {'progress', 'time', 'score', 'powerup', 'completion', 'death'},
                set(info['reward_components']),
            )
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
            self.assertFalse(info['clear'])
            self.assertFalse(info['death'])
            self.assertEqual('smb3', info['game'])
            self.assertTrue(info['single_stage'])
            self.assertEqual('SuperMarioBros3-1-1-v0', info['task_id'])
            self.assertEqual(1, info['target_world'])
            self.assertEqual(1, info['target_stage'])
        finally:
            env.close()

    def test_validated_world_1_stage_targets(self):
        for stage in (2, 4, 6):
            env = SuperMarioBros3Env(target=(1, stage), render_mode='rgb_array')
            try:
                self.assertTrue(env.unwrapped.is_single_stage_env)
                self.assertEqual(1, env.unwrapped._target_world)
                self.assertEqual(stage, env.unwrapped._target_stage)

                state, reset_info = env.reset()
                self.assertEqual(env.observation_space.shape, state.shape)
                self.assertIsInstance(reset_info, dict)

                state, reward, terminated, truncated, info = env.step(0)
                self.assertEqual(env.observation_space.shape, state.shape)
                self.assertEqual(0.0, reward)
                self.assertFalse(terminated)
                self.assertFalse(truncated)
                self.assertTrue(info['in_level'])
                self.assertEqual(1, info['world'])
                self.assertEqual(stage, info['stage'])
                self.assertEqual(
                    'SuperMarioBros3-1-{}-v0'.format(stage),
                    info['task_id'],
                )
                self.assertEqual(1, info['target_world'])
                self.assertEqual(stage, info['target_stage'])
            finally:
                env.close()


class ShouldRenderSuperMarioBros3StatusBar(TestCase):
    """Regression coverage for MMC3 status-bar CHR banking in SMB3."""

    def test_world_1_stage_2_status_bar_tiles_are_stable(self):
        env = SuperMarioBros3Env(target=(1, 2), render_mode='rgb_array')
        try:
            env.reset()
            state, _, _, _, info = env.step(0)
            self.assertEqual('SuperMarioBros3-1-2-v0', info['task_id'])

            expected_pixels = {
                (200, 13): (252, 252, 252),
                (200, 21): (0, 0, 0),
                (201, 16): (0, 252, 252),
                (201, 48): (0, 252, 252),
                (203, 96): (0, 252, 252),
                (208, 8): (0, 0, 0),
                (224, 208): (0, 0, 0),
                (227, 10): (0, 0, 0),
            }
            for (y, x), expected in expected_pixels.items():
                with self.subTest(pixel=(y, x)):
                    self.assertEqual(expected, tuple(map(int, state[y, x])))
        finally:
            env.close()

    def test_status_bar_baseline_stays_fixed_while_stage_scrolls(self):
        env = SuperMarioBros3Env(render_mode='rgb_array')
        try:
            env.reset(seed=17)
            for step in range(241):
                state, _, terminated, truncated, _ = env.step(128)
                self.assertFalse(terminated)
                self.assertFalse(truncated)
                if step in (0, 60, 120, 180, 240):
                    with self.subTest(step=step):
                        self.assertEqual((0, 0, 0), tuple(map(int, state[227, 10])))
                        self.assertEqual((0, 0, 0), tuple(map(int, state[224, 10])))
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

    def test_reward_diagnostics_match_clipped_step_reward(self):
        env = SuperMarioBros3Env(render_mode='rgb_array')
        try:
            env.reset()
            env.ram[0x0090] = 27

            reward = env.unwrapped._get_reward()
            info = env.unwrapped._reward_info()

            self.assertEqual(3.0, reward)
            self.assertEqual(3.0, info['reward_components']['progress'])
            self.assertEqual(3.0, info['reward_total_unclipped'])
            self.assertEqual(3.0, info['reward_total_clipped'])
        finally:
            env.close()


class ShouldTerminateSuperMarioBros3Env(TestCase):
    """Test stage-return, death, and game-over termination helpers."""

    def test_stage_env_step_returns_positive_clear_reward(self):
        env = SuperMarioBros3Env(target=(1, 1), render_mode='rgb_array')
        try:
            env.reset()
            env.unwrapped._entered_level = True
            env.unwrapped._life_start = 4
            env.unwrapped._life_last = 4
            env.ram[0x0736] = 4
            env.ram[0x05ee] = 0
            env.ram[0x05ef] = 0
            env.ram[0x05f0] = 0
            env.ram[0x0075] = 0x20
            env.ram[0x0079] = 0x40

            _, reward, terminated, truncated, info = env.step(0)

            self.assertTrue(terminated)
            self.assertFalse(truncated)
            self.assertEqual(15, reward)
            self.assertTrue(info['flag_get'])
            self.assertTrue(info['clear'])
            self.assertFalse(info['death'])
            self.assertEqual(0.0, info['reward_components']['time'])
            self.assertEqual(50.0, info['reward_components']['completion'])
            self.assertEqual(50.0, info['reward_total_unclipped'])
            self.assertEqual(15.0, info['reward_total_clipped'])
        finally:
            env.close()

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

    def test_full_env_life_loss_returns_to_map_without_clear_latch(self):
        env = SuperMarioBros3Env(render_mode='rgb_array')
        try:
            env.reset()
            env.ram[0x00b4] = 0xc0
            death_step = None

            for _ in range(360):
                _, reward, terminated, truncated, info = env.step(0)
                if info['death']:
                    death_step = reward, terminated, truncated, info
                    break

            self.assertIsNotNone(death_step)
            reward, terminated, truncated, info = death_step
            self.assertEqual(-15, reward)
            self.assertFalse(terminated)
            self.assertFalse(truncated)
            self.assertFalse(info['flag_get'])
            self.assertFalse(info['clear'])
            self.assertTrue(info['death'])
            self.assertFalse(info['in_level'])
            self.assertEqual(3, info['life'])

            _, reward, terminated, truncated, info = env.step(0)
            self.assertEqual(0.0, reward)
            self.assertFalse(terminated)
            self.assertFalse(truncated)
            self.assertFalse(info['flag_get'])
            self.assertFalse(info['clear'])
            self.assertFalse(info['death'])
            self.assertFalse(info['in_level'])
            self.assertEqual(3, info['life'])
        finally:
            env.close()
