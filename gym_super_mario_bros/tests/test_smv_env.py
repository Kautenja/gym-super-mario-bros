"""Test cases for the Super Mario Bros meta environment."""
from unittest import TestCase
from .._roms.decode_target import decode_target
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
        self.assertRaises(ValueError, SuperMarioBrosEnv, target=(14, 1), lost_levels=True)


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


class ShouldDecodeLostLevelsBonusWorldTargets(TestCase):
    def test(self):
        for world in range(5, 14):
            for stage in range(1, 5):
                self.assertEqual(
                    (world, stage, stage),
                    decode_target((world, stage), lost_levels=True),
                )


class ShouldStepGameEnv(TestCase):
    def test(self):
        env = SuperMarioBrosEnv(render_mode='rgb_array')
        self.assertFalse(env.unwrapped.is_single_stage_env)
        self.assertIsNone(env.unwrapped._target_world)
        self.assertIsNone(env.unwrapped._target_stage)
        self.assertIsNone(env.unwrapped._target_area)
        reset_result = env.reset()
        self.assertEqual(2, len(reset_result))
        state, reset_info = reset_result
        self.assertEqual(env.observation_space.shape, state.shape)
        self.assertIsInstance(reset_info, dict)
        step_result = env.step(0)
        self.assertEqual(5, len(step_result))
        s, r, terminated, truncated, i = step_result
        self.assertEqual(env.observation_space.shape, s.shape)
        self.assertIsInstance(terminated, bool)
        self.assertIsInstance(truncated, bool)
        self.assertFalse(truncated)
        self.assertIsNotNone(env.render())
        self.assertEqual(0, i['coins'])
        self.assertEqual(False, i['flag_get'])
        self.assertEqual(2, i['life'])
        self.assertEqual(1, i['world'])
        self.assertEqual(0, i['score'])
        self.assertEqual(1, i['stage'])
        self.assertEqual(400, i['time'])
        self.assertEqual(40, i['x_pos'])
        self.assertEqual(1, i['area'])
        self.assertEqual((0, 0, 0, 0, 0), i['enemy_types'])
        self.assertFalse(i['is_dead'])
        self.assertFalse(i['is_dying'])
        self.assertFalse(i['is_game_over'])
        self.assertFalse(i['is_stage_over'])
        self.assertFalse(i['is_world_over'])
        self.assertEqual(40, i['left_x_pos'])
        self.assertEqual(0, i['level'])
        self.assertEqual(8, i['player_state'])
        self.assertEqual(0, i['powerup_level'])
        self.assertEqual(0, i['status_value'])
        self.assertEqual(40, i['x_pos_max'])
        self.assertEqual(176, i['y_pixel'])
        self.assertEqual(79, i['y_pos'])
        self.assertEqual(1, i['y_viewport'])
        env.close()


class ShouldStepStageEnv(TestCase):
    def test(self):
        env = SuperMarioBrosEnv(target=(4, 2), render_mode='rgb_array')
        self.assertTrue(env.unwrapped.is_single_stage_env)
        self.assertIsInstance(env.unwrapped._target_world, int)
        self.assertIsInstance(env.unwrapped._target_stage, int)
        self.assertIsInstance(env.unwrapped._target_area, int)
        reset_result = env.reset()
        self.assertEqual(2, len(reset_result))
        state, reset_info = reset_result
        self.assertEqual(env.observation_space.shape, state.shape)
        self.assertIsInstance(reset_info, dict)
        step_result = env.step(0)
        self.assertEqual(5, len(step_result))
        s, r, terminated, truncated, i = step_result
        self.assertEqual(env.observation_space.shape, s.shape)
        self.assertIsInstance(terminated, bool)
        self.assertIsInstance(truncated, bool)
        self.assertFalse(truncated)
        self.assertIsNotNone(env.render())
        self.assertEqual(0, i['coins'])
        self.assertEqual(False, i['flag_get'])
        self.assertEqual(2, i['life'])
        self.assertEqual(4, i['world'])
        self.assertEqual(0, i['score'])
        self.assertEqual(2, i['stage'])
        self.assertEqual(400, i['time'])
        self.assertEqual(40, i['x_pos'])
        self.assertEqual(13, i['level'])
        self.assertEqual(40, i['x_pos_max'])
        env.close()


class ShouldRewardSuperMarioBrosObjectives(TestCase):
    """Test objective reward shaping for SMB1 and Lost Levels."""

    def test_new_best_progress_does_not_penalize_backtracking(self):
        env = SuperMarioBrosEnv(render_mode='rgb_array')
        try:
            env.reset()
            env.ram[0x0086] = 43
            self.assertEqual(3, env.unwrapped._progress_reward)

            env.ram[0x0086] = 41
            self.assertEqual(0, env.unwrapped._progress_reward)
        finally:
            env.close()

    def test_score_coin_powerup_and_completion_rewards(self):
        env = SuperMarioBrosEnv(render_mode='rgb_array')
        try:
            env.reset()

            env.unwrapped._score_last = 0
            env.ram[0x07de:0x07e4] = [0, 0, 0, 1, 0, 0]
            self.assertEqual(1, env.unwrapped._score_reward)

            env.unwrapped._coins_last = 0
            env.ram[0x07ed:0x07ef] = [0, 1]
            self.assertEqual(5, env.unwrapped._coin_reward)

            env.unwrapped._status_last = 0
            env.ram[0x0756] = 1
            self.assertEqual(5, env.unwrapped._powerup_reward)

            env.ram[0x0756] = 0
            self.assertEqual(-5, env.unwrapped._powerup_reward)

            env.ram[0x0016] = 0x31
            env.ram[0x001d] = 3
            self.assertEqual(50, env.unwrapped._completion_reward)
            self.assertEqual(0, env.unwrapped._completion_reward)
        finally:
            env.close()
