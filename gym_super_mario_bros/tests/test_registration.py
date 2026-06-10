"""Test cases for the Gymnasium registered environments."""
from unittest import TestCase

import gymnasium as gym
import gym_super_mario_bros

from .. import _registration
from .._registration import make


_SMB2_USA_STAGES_PER_WORLD = (3, 3, 3, 3, 3, 3, 2)
_SMB3_STAGE_IDS = ('SuperMarioBros3-1-1-v0',)


def _expected_stage_ids():
    """Return the historical stage IDs plus the separator-free aliases."""
    for world in range(1, 9):
        for stage in range(1, 5):
            yield 'SuperMarioBros-{}-{}-v0'.format(world, stage)
            yield 'SuperMarioBros{}-{}-v0'.format(world, stage)


def _lost_levels_world_label(world):
    """Return the public world label for Lost Levels stage IDs."""
    if world <= 9:
        return str(world)
    return chr(ord('A') + world - 10)


def _expected_lost_levels_stage_ids():
    """Return the registered Lost Levels stage IDs."""
    for world in range(1, 14):
        label = _lost_levels_world_label(world)
        for stage in range(1, 5):
            yield 'SuperMarioBros2-{}-{}-v0'.format(label, stage)


def _expected_smb2_usa_stage_ids():
    """Return the registered Super Mario Bros. 2 (USA) stage IDs."""
    for world, stage_count in enumerate(_SMB2_USA_STAGES_PER_WORLD, start=1):
        for stage in range(1, stage_count + 1):
            yield 'SuperMarioBros2USA-{}-{}-v0'.format(world, stage)


def _expected_smb3_stage_ids():
    """Return the registered Super Mario Bros. 3 stage IDs."""
    yield from _SMB3_STAGE_IDS


class ShouldExposePackageApi(TestCase):
    """Test package-level public API and Gymnasium make alias."""

    def test_make_alias_is_gymnasium_make(self):
        self.assertIs(make, gym.make)
        self.assertIs(gym_super_mario_bros.make, gym.make)

    def test_all_is_stable(self):
        self.assertEqual(['make'], _registration.__all__)
        self.assertEqual(
            [
                'make',
                'SuperMarioBrosEnv',
                'SuperMarioBros2Env',
                'SuperMarioBros3Env',
                'MarioTask',
                'all_tasks',
                'task_for_env_id',
                'task_ids',
            ],
            gym_super_mario_bros.__all__,
        )


class ShouldRegisterExpectedGymnasiumEnvs(TestCase):
    """Test that Gymnasium registration metadata remains stable."""

    def _assert_common_registration_policy(self, env_id):
        spec = gym.spec(env_id)
        self.assertEqual(_registration._MAX_EPISODE_STEPS, spec.max_episode_steps)
        self.assertEqual(_registration._REWARD_THRESHOLD, spec.reward_threshold)
        self.assertTrue(spec.nondeterministic)
        self.assertTrue(spec.disable_env_checker)

    def test_env_checker_policy_is_explicit(self):
        self.assertTrue(_registration._DISABLE_ENV_CHECKER)
        self.assertIn('ROM-backed NES', _registration._DISABLE_ENV_CHECKER_REASON)
        self.assertIn(
            'Gymnasium passive checker',
            _registration._DISABLE_ENV_CHECKER_REASON,
        )

    def test_core_ids_are_registered_unchanged(self):
        env_id = 'SuperMarioBros-v0'
        spec = gym.spec(env_id)
        self.assertEqual(
            'gym_super_mario_bros:SuperMarioBrosEnv',
            spec.entry_point,
        )
        self.assertEqual({}, spec.kwargs)
        self._assert_common_registration_policy(env_id)

    def test_lost_levels_ids_are_registered_unchanged(self):
        env_id = 'SuperMarioBros2-v0'
        spec = gym.spec(env_id)
        self.assertEqual(
            'gym_super_mario_bros:SuperMarioBrosEnv',
            spec.entry_point,
        )
        self.assertEqual({'lost_levels': True}, spec.kwargs)
        self._assert_common_registration_policy(env_id)

    def test_smb2_usa_id_is_registered(self):
        env_id = 'SuperMarioBros2USA-v0'
        spec = gym.spec(env_id)
        self.assertEqual(
            'gym_super_mario_bros:SuperMarioBros2Env',
            spec.entry_point,
        )
        self.assertEqual({}, spec.kwargs)
        self._assert_common_registration_policy(env_id)

    def test_smb3_id_is_registered(self):
        env_id = 'SuperMarioBros3-v0'
        spec = gym.spec(env_id)
        self.assertEqual(
            'gym_super_mario_bros:SuperMarioBros3Env',
            spec.entry_point,
        )
        self.assertEqual({}, spec.kwargs)
        self._assert_common_registration_policy(env_id)

    def test_stage_ids_and_aliases_are_registered_unchanged(self):
        stage_ids = list(_expected_stage_ids())
        self.assertEqual(64, len(stage_ids))
        for env_id in stage_ids:
            spec = gym.spec(env_id)
            self.assertEqual(
                'gym_super_mario_bros:SuperMarioBrosEnv',
                spec.entry_point,
            )
            self.assertNotIn('rom_mode', spec.kwargs)
            self.assertIn('target', spec.kwargs)
            self._assert_common_registration_policy(env_id)

    def test_lost_levels_stage_ids_are_registered(self):
        stage_ids = list(_expected_lost_levels_stage_ids())
        self.assertEqual(52, len(stage_ids))
        for env_id in stage_ids:
            spec = gym.spec(env_id)
            self.assertEqual(
                'gym_super_mario_bros:SuperMarioBrosEnv',
                spec.entry_point,
            )
            self.assertTrue(spec.kwargs['lost_levels'])
            self.assertNotIn('rom_mode', spec.kwargs)
            self.assertIn('target', spec.kwargs)
            self._assert_common_registration_policy(env_id)

    def test_smb2_usa_stage_ids_are_registered(self):
        stage_ids = list(_expected_smb2_usa_stage_ids())
        self.assertEqual(20, len(stage_ids))
        for env_id in stage_ids:
            spec = gym.spec(env_id)
            self.assertEqual(
                'gym_super_mario_bros:SuperMarioBros2Env',
                spec.entry_point,
            )
            self.assertIn('target', spec.kwargs)
            self._assert_common_registration_policy(env_id)

    def test_smb3_stage_ids_are_registered(self):
        stage_ids = list(_expected_smb3_stage_ids())
        self.assertEqual(1, len(stage_ids))
        for env_id in stage_ids:
            spec = gym.spec(env_id)
            self.assertEqual(
                'gym_super_mario_bros:SuperMarioBros3Env',
                spec.entry_point,
            )
            self.assertEqual({'target': (1, 1)}, spec.kwargs)
            self._assert_common_registration_policy(env_id)

    def test_removed_variant_ids_are_not_registered(self):
        for env_id in (
            'SuperMarioBros-v1',
            'SuperMarioBros-v2',
            'SuperMarioBros-v3',
            'SuperMarioBrosRandomStages-v0',
            'SuperMarioBrosRandomStages-v1',
            'SuperMarioBrosRandomStages-v2',
            'SuperMarioBrosRandomStages-v3',
            'SuperMarioBros2-v1',
            'SuperMarioBros-1-1-v1',
            'SuperMarioBros1-1-v1',
            'SuperMarioBros2-1-1-v1',
        ):
            self.assertNotIn(env_id, gym.envs.registration.registry)


class ShouldSmokeRepresentativeRegisteredEnvs(TestCase):
    """Test representative Gymnasium creation, reset, step, render, and close."""

    def test(self):
        for env_id in (
            'SuperMarioBros-v0',
            'SuperMarioBros1-1-v0',
            'SuperMarioBros2USA-v0',
            'SuperMarioBros3-v0',
        ):
            env = gym.make(env_id, render_mode='rgb_array')
            try:
                state, info = env.reset(seed=123)
                self.assertEqual(env.observation_space.shape, state.shape)
                self.assertIsInstance(info, dict)
                self.assertEqual(5, len(env.step(env.action_space.sample())))
                self.assertIsNotNone(env.render())
            finally:
                env.close()


class ShouldMakeEnv:
    """A test case for making an arbitrary environment."""
    # the number of coins at the start
    coins = 0
    # whether flag get is thrown
    flag_get = False
    # the number of lives left
    life = 2
    # the current world
    world = 1
    # the current score
    score = 0
    # the current stage
    stage = 1
    # the amount of time left
    time = 400
    # the x position of Mario
    x_pos = 40
    # the environments ID
    env_id = None
    # the random seed to apply
    seed = None

    def _test_env(self, env_id):
        env = make(env_id, render_mode='rgb_array')
        reset_result = env.reset(seed=self.seed)
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
        self.assertEqual(self.coins, i['coins'])
        self.assertEqual(self.flag_get, i['flag_get'])
        self.assertEqual(self.life, i['life'])
        self.assertEqual(self.world, i['world'])
        self.assertEqual(self.score, i['score'])
        self.assertEqual(self.stage, i['stage'])
        self.assertEqual(self.time, i['time'])
        self.assertEqual(self.x_pos, i['x_pos'])
        env.close()

    def test(self):
        self._test_env(self.env_id)


class ShouldMakeSuperMarioBros(ShouldMakeEnv, TestCase):
    # the environment ID for Super Mario Bros
    env_id = 'SuperMarioBros-v0'


class ShouldTruncateWithGymnasiumTimeLimit(TestCase):
    def test(self):
        env = make(
            'SuperMarioBros-v0',
            render_mode='rgb_array',
            max_episode_steps=1,
        )
        try:
            env.reset(seed=123)
            _, _, terminated, truncated, _ = env.step(0)
            self.assertFalse(terminated)
            self.assertTrue(truncated)
        finally:
            env.close()


class ShouldMakeSuperMarioBrosLostLevels(ShouldMakeEnv, TestCase):
    # the amount of time left
    time = 400
    # the environment ID for Super Mario Bros. 2 (Japan)
    env_id = 'SuperMarioBros2-v0'


class ShouldMakeLostLevels_5_1(ShouldMakeEnv, TestCase):
    world = 5
    stage = 1
    env_id = 'SuperMarioBros2-5-1-v0'


class ShouldMakeLostLevels_8_4(ShouldMakeEnv, TestCase):
    world = 8
    stage = 4
    env_id = 'SuperMarioBros2-8-4-v0'


class ShouldMakeLostLevels_A_2(ShouldMakeEnv, TestCase):
    time = 300
    world = 10
    stage = 2
    env_id = 'SuperMarioBros2-A-2-v0'


class ShouldMakeLostLevels_D_4(ShouldMakeEnv, TestCase):
    world = 13
    stage = 4
    env_id = 'SuperMarioBros2-D-4-v0'


class ShouldMakeSuperMarioBros_1_1(ShouldMakeEnv, TestCase):
    # the current world
    world = 1
    # the current stage
    stage = 1
    # the environments ID
    env_id = 'SuperMarioBros-1-1-v0'


class ShouldMakeSuperMarioBrosAlias_1_1(ShouldMakeEnv, TestCase):
    # the current world
    world = 1
    # the current stage
    stage = 1
    # the environments ID
    env_id = 'SuperMarioBros1-1-v0'


class ShouldMakeSuperMarioBros_1_2(ShouldMakeEnv, TestCase):
    # the current world
    world = 1
    # the current stage
    stage = 2
    # the environments ID
    env_id = 'SuperMarioBros-1-2-v0'


class ShouldMakeSuperMarioBros_1_3(ShouldMakeEnv, TestCase):
    # the amount of time left
    time = 300
    # the current world
    world = 1
    # the current stage
    stage = 3
    # the environments ID
    env_id = 'SuperMarioBros-1-3-v0'


class ShouldMakeSuperMarioBros_1_4(ShouldMakeEnv, TestCase):
    # the amount of time left
    time = 300
    # the current world
    world = 1
    # the current stage
    stage = 4
    # the environments ID
    env_id = 'SuperMarioBros-1-4-v0'


class ShouldMakeSuperMarioBros_2_1(ShouldMakeEnv, TestCase):
    # the current world
    world = 2
    # the current stage
    stage = 1
    # the environments ID
    env_id = 'SuperMarioBros-2-1-v0'


class ShouldMakeSuperMarioBros_2_2(ShouldMakeEnv, TestCase):
    # the current world
    world = 2
    # the current stage
    stage = 2
    # the environments ID
    env_id = 'SuperMarioBros-2-2-v0'


class ShouldMakeSuperMarioBros_2_3(ShouldMakeEnv, TestCase):
    # the amount of time left
    time = 300
    # the current world
    world = 2
    # the current stage
    stage = 3
    # the environments ID
    env_id = 'SuperMarioBros-2-3-v0'


class ShouldMakeSuperMarioBros_2_4(ShouldMakeEnv, TestCase):
    # the amount of time left
    time = 300
    # the current world
    world = 2
    # the current stage
    stage = 4
    # the environments ID
    env_id = 'SuperMarioBros-2-4-v0'


class ShouldMakeSuperMarioBros_3_1(ShouldMakeEnv, TestCase):
    # the current world
    world = 3
    # the current stage
    stage = 1
    # the environments ID
    env_id = 'SuperMarioBros-3-1-v0'


class ShouldMakeSuperMarioBros_3_2(ShouldMakeEnv, TestCase):
    # the amount of time left
    time = 300
    # the current world
    world = 3
    # the current stage
    stage = 2
    # the environments ID
    env_id = 'SuperMarioBros-3-2-v0'


class ShouldMakeSuperMarioBros_3_3(ShouldMakeEnv, TestCase):
    # the amount of time left
    time = 300
    # the current world
    world = 3
    # the current stage
    stage = 3
    # the environments ID
    env_id = 'SuperMarioBros-3-3-v0'


class ShouldMakeSuperMarioBros_3_4(ShouldMakeEnv, TestCase):
    # the amount of time left
    time = 300
    # the current world
    world = 3
    # the current stage
    stage = 4
    # the environments ID
    env_id = 'SuperMarioBros-3-4-v0'


class ShouldMakeSuperMarioBros_4_1(ShouldMakeEnv, TestCase):
    # the current world
    world = 4
    # the current stage
    stage = 1
    # the environments ID
    env_id = 'SuperMarioBros-4-1-v0'


class ShouldMakeSuperMarioBros_4_2(ShouldMakeEnv, TestCase):
    # the current world
    world = 4
    # the current stage
    stage = 2
    # the environments ID
    env_id = 'SuperMarioBros-4-2-v0'


class ShouldMakeSuperMarioBros_4_3(ShouldMakeEnv, TestCase):
    # the amount of time left
    time = 300
    # the current world
    world = 4
    # the current stage
    stage = 3
    # the environments ID
    env_id = 'SuperMarioBros-4-3-v0'


class ShouldMakeSuperMarioBros_4_4(ShouldMakeEnv, TestCase):
    # the current world
    world = 4
    # the current stage
    stage = 4
    # the environments ID
    env_id = 'SuperMarioBros-4-4-v0'


class ShouldMakeSuperMarioBros_5_1(ShouldMakeEnv, TestCase):
    # the amount of time left
    time = 300
    # the current world
    world = 5
    # the current stage
    stage = 1
    # the environments ID
    env_id = 'SuperMarioBros-5-1-v0'


class ShouldMakeSuperMarioBros_5_2(ShouldMakeEnv, TestCase):
    # the current world
    world = 5
    # the current stage
    stage = 2
    # the environments ID
    env_id = 'SuperMarioBros-5-2-v0'


class ShouldMakeSuperMarioBros_5_3(ShouldMakeEnv, TestCase):
    # the amount of time left
    time = 300
    # the current world
    world = 5
    # the current stage
    stage = 3
    # the environments ID
    env_id = 'SuperMarioBros-5-3-v0'


class ShouldMakeSuperMarioBros_5_4(ShouldMakeEnv, TestCase):
    # the amount of time left
    time = 300
    # the current world
    world = 5
    # the current stage
    stage = 4
    # the environments ID
    env_id = 'SuperMarioBros-5-4-v0'


class ShouldMakeSuperMarioBros_6_1(ShouldMakeEnv, TestCase):
    # the current world
    world = 6
    # the current stage
    stage = 1
    # the environments ID
    env_id = 'SuperMarioBros-6-1-v0'


class ShouldMakeSuperMarioBros_6_2(ShouldMakeEnv, TestCase):
    # the current world
    world = 6
    # the current stage
    stage = 2
    # the environments ID
    env_id = 'SuperMarioBros-6-2-v0'


class ShouldMakeSuperMarioBros_6_3(ShouldMakeEnv, TestCase):
    # the amount of time left
    time = 300
    # the current world
    world = 6
    # the current stage
    stage = 3
    # the environments ID
    env_id = 'SuperMarioBros-6-3-v0'


class ShouldMakeSuperMarioBros_6_4(ShouldMakeEnv, TestCase):
    # the amount of time left
    time = 300
    # the current world
    world = 6
    # the current stage
    stage = 4
    # the environments ID
    env_id = 'SuperMarioBros-6-4-v0'


class ShouldMakeSuperMarioBros_7_1(ShouldMakeEnv, TestCase):
    # the current world
    world = 7
    # the current stage
    stage = 1
    # the environments ID
    env_id = 'SuperMarioBros-7-1-v0'


class ShouldMakeSuperMarioBros_7_2(ShouldMakeEnv, TestCase):
    # the current world
    world = 7
    # the current stage
    stage = 2
    # the environments ID
    env_id = 'SuperMarioBros-7-2-v0'


class ShouldMakeSuperMarioBros_7_3(ShouldMakeEnv, TestCase):
    # the amount of time left
    time = 300
    # the current world
    world = 7
    # the current stage
    stage = 3
    # the environments ID
    env_id = 'SuperMarioBros-7-3-v0'


class ShouldMakeSuperMarioBros_7_4(ShouldMakeEnv, TestCase):
    # the current world
    world = 7
    # the current stage
    stage = 4
    # the environments ID
    env_id = 'SuperMarioBros-7-4-v0'


class ShouldMakeSuperMarioBros_8_1(ShouldMakeEnv, TestCase):
    # the amount of time left
    time = 300
    # the current world
    world = 8
    # the current stage
    stage = 1
    # the environments ID
    env_id = 'SuperMarioBros-8-1-v0'


class ShouldMakeSuperMarioBros_8_2(ShouldMakeEnv, TestCase):
    # the current world
    world = 8
    # the current stage
    stage = 2
    # the environments ID
    env_id = 'SuperMarioBros-8-2-v0'


class ShouldMakeSuperMarioBros_8_3(ShouldMakeEnv, TestCase):
    # the amount of time left
    time = 300
    # the current world
    world = 8
    # the current stage
    stage = 3
    # the environments ID
    env_id = 'SuperMarioBros-8-3-v0'


class ShouldMakeSuperMarioBros_8_4(ShouldMakeEnv, TestCase):
    # the current world
    world = 8
    # the current stage
    stage = 4
    # the environments ID
    env_id = 'SuperMarioBros-8-4-v0'
