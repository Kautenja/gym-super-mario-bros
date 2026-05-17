"""Test cases for the Gymnasium registered environments."""
from unittest import TestCase
from .._registration import make


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
    # the subset of stages to sample from
    stages = None

    def _test_env(self, env_id, stages):
        if stages is not None:
            env = make(env_id, stages=stages, render_mode='rgb_array')
        else:
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
        if isinstance(self.env_id, str):
            self._test_env(self.env_id, self.stages)
        elif isinstance(self.env_id, list):
            for env_id in self.env_id:
                self._test_env(env_id, self.stages)


class ShouldMakeSuperMarioBros(ShouldMakeEnv, TestCase):
    # the environments ID for all versions of Super Mario Bros
    env_id = ['SuperMarioBros-v{}'.format(v) for v in range(4)]


class ShouldMakeSuperMarioBrosRandomStages(ShouldMakeEnv, TestCase):
    # the random number seed for this environment
    seed = 1
    # the amount of time left
    time = 300
    # the current world
    world = 4
    # the current stage
    stage = 3
    # the environments ID for all versions of Super Mario Bros
    env_id = ['SuperMarioBrosRandomStages-v{}'.format(v) for v in range(4)]


class ShouldReproduceSuperMarioBrosRandomStages(TestCase):
    def _selected_stage(self, seed, options=None):
        env = make('SuperMarioBrosRandomStages-v0', render_mode='rgb_array')
        try:
            _, info = env.reset(seed=seed, options=options)
            return info['world'], info['stage']
        finally:
            env.close()

    def test_fixed_seed_is_reproducible(self):
        first_stage = self._selected_stage(seed=123)
        second_stage = self._selected_stage(seed=123)
        self.assertEqual(first_stage, second_stage)

    def test_options_can_override_stage_subset(self):
        stage = self._selected_stage(
            seed=123,
            options={'stages': ['4-2']},
        )
        self.assertEqual((4, 2), stage)


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
    # the environments ID for all versions of Super Mario Bros
    env_id = ['SuperMarioBros2-v{}'.format(v) for v in range(2)]


class ShouldMakeSuperMarioBros_1_1(ShouldMakeEnv, TestCase):
    # the current world
    world = 1
    # the current stage
    stage = 1
    # the environments ID
    env_id = ['SuperMarioBros-1-1-v{}'.format(v) for v in range(4)]


class ShouldMakeSuperMarioBrosAlias_1_1(ShouldMakeEnv, TestCase):
    # the current world
    world = 1
    # the current stage
    stage = 1
    # the environments ID
    env_id = ['SuperMarioBros1-1-v{}'.format(v) for v in range(4)]


class ShouldMakeSuperMarioBros_1_2(ShouldMakeEnv, TestCase):
    # the current world
    world = 1
    # the current stage
    stage = 2
    # the environments ID
    env_id = ['SuperMarioBros-1-2-v{}'.format(v) for v in range(4)]


class ShouldMakeSuperMarioBros_1_3(ShouldMakeEnv, TestCase):
    # the amount of time left
    time = 300
    # the current world
    world = 1
    # the current stage
    stage = 3
    # the environments ID
    env_id = ['SuperMarioBros-1-3-v{}'.format(v) for v in range(4)]


class ShouldMakeSuperMarioBros_1_4(ShouldMakeEnv, TestCase):
    # the amount of time left
    time = 300
    # the current world
    world = 1
    # the current stage
    stage = 4
    # the environments ID
    env_id = ['SuperMarioBros-1-4-v{}'.format(v) for v in range(4)]


class ShouldMakeSuperMarioBros_2_1(ShouldMakeEnv, TestCase):
    # the current world
    world = 2
    # the current stage
    stage = 1
    # the environments ID
    env_id = ['SuperMarioBros-2-1-v{}'.format(v) for v in range(4)]


class ShouldMakeSuperMarioBros_2_2(ShouldMakeEnv, TestCase):
    # the current world
    world = 2
    # the current stage
    stage = 2
    # the environments ID
    env_id = ['SuperMarioBros-2-2-v{}'.format(v) for v in range(4)]


class ShouldMakeSuperMarioBros_2_3(ShouldMakeEnv, TestCase):
    # the amount of time left
    time = 300
    # the current world
    world = 2
    # the current stage
    stage = 3
    # the environments ID
    env_id = ['SuperMarioBros-2-3-v{}'.format(v) for v in range(4)]


class ShouldMakeSuperMarioBros_2_4(ShouldMakeEnv, TestCase):
    # the amount of time left
    time = 300
    # the current world
    world = 2
    # the current stage
    stage = 4
    # the environments ID
    env_id = ['SuperMarioBros-2-4-v{}'.format(v) for v in range(4)]


class ShouldMakeSuperMarioBros_3_1(ShouldMakeEnv, TestCase):
    # the current world
    world = 3
    # the current stage
    stage = 1
    # the environments ID
    env_id = ['SuperMarioBros-3-1-v{}'.format(v) for v in range(4)]


class ShouldMakeSuperMarioBros_3_2(ShouldMakeEnv, TestCase):
    # the amount of time left
    time = 300
    # the current world
    world = 3
    # the current stage
    stage = 2
    # the environments ID
    env_id = ['SuperMarioBros-3-2-v{}'.format(v) for v in range(4)]


class ShouldMakeSuperMarioBros_3_3(ShouldMakeEnv, TestCase):
    # the amount of time left
    time = 300
    # the current world
    world = 3
    # the current stage
    stage = 3
    # the environments ID
    env_id = ['SuperMarioBros-3-3-v{}'.format(v) for v in range(4)]


class ShouldMakeSuperMarioBros_3_4(ShouldMakeEnv, TestCase):
    # the amount of time left
    time = 300
    # the current world
    world = 3
    # the current stage
    stage = 4
    # the environments ID
    env_id = ['SuperMarioBros-3-4-v{}'.format(v) for v in range(4)]


class ShouldMakeSuperMarioBros_4_1(ShouldMakeEnv, TestCase):
    # the current world
    world = 4
    # the current stage
    stage = 1
    # the environments ID
    env_id = ['SuperMarioBros-4-1-v{}'.format(v) for v in range(4)]


class ShouldMakeSuperMarioBros_4_2(ShouldMakeEnv, TestCase):
    # the current world
    world = 4
    # the current stage
    stage = 2
    # the environments ID
    env_id = ['SuperMarioBros-4-2-v{}'.format(v) for v in range(4)]


class ShouldMakeSuperMarioBros_4_3(ShouldMakeEnv, TestCase):
    # the amount of time left
    time = 300
    # the current world
    world = 4
    # the current stage
    stage = 3
    # the environments ID
    env_id = ['SuperMarioBros-4-3-v{}'.format(v) for v in range(4)]


class ShouldMakeSuperMarioBros_4_4(ShouldMakeEnv, TestCase):
    # the current world
    world = 4
    # the current stage
    stage = 4
    # the environments ID
    env_id = ['SuperMarioBros-4-4-v{}'.format(v) for v in range(4)]


class ShouldMakeSuperMarioBros_5_1(ShouldMakeEnv, TestCase):
    # the amount of time left
    time = 300
    # the current world
    world = 5
    # the current stage
    stage = 1
    # the environments ID
    env_id = ['SuperMarioBros-5-1-v{}'.format(v) for v in range(4)]


class ShouldMakeSuperMarioBros_5_2(ShouldMakeEnv, TestCase):
    # the current world
    world = 5
    # the current stage
    stage = 2
    # the environments ID
    env_id = ['SuperMarioBros-5-2-v{}'.format(v) for v in range(4)]


class ShouldMakeSuperMarioBros_5_3(ShouldMakeEnv, TestCase):
    # the amount of time left
    time = 300
    # the current world
    world = 5
    # the current stage
    stage = 3
    # the environments ID
    env_id = ['SuperMarioBros-5-3-v{}'.format(v) for v in range(4)]


class ShouldMakeSuperMarioBros_5_4(ShouldMakeEnv, TestCase):
    # the amount of time left
    time = 300
    # the current world
    world = 5
    # the current stage
    stage = 4
    # the environments ID
    env_id = ['SuperMarioBros-5-4-v{}'.format(v) for v in range(4)]


class ShouldMakeSuperMarioBros_6_1(ShouldMakeEnv, TestCase):
    # the current world
    world = 6
    # the current stage
    stage = 1
    # the environments ID
    env_id = ['SuperMarioBros-6-1-v{}'.format(v) for v in range(4)]


class ShouldMakeSuperMarioBros_6_2(ShouldMakeEnv, TestCase):
    # the current world
    world = 6
    # the current stage
    stage = 2
    # the environments ID
    env_id = ['SuperMarioBros-6-2-v{}'.format(v) for v in range(4)]


class ShouldMakeSuperMarioBros_6_3(ShouldMakeEnv, TestCase):
    # the amount of time left
    time = 300
    # the current world
    world = 6
    # the current stage
    stage = 3
    # the environments ID
    env_id = ['SuperMarioBros-6-3-v{}'.format(v) for v in range(4)]


class ShouldMakeSuperMarioBros_6_4(ShouldMakeEnv, TestCase):
    # the amount of time left
    time = 300
    # the current world
    world = 6
    # the current stage
    stage = 4
    # the environments ID
    env_id = ['SuperMarioBros-6-4-v{}'.format(v) for v in range(4)]


class ShouldMakeSuperMarioBros_7_1(ShouldMakeEnv, TestCase):
    # the current world
    world = 7
    # the current stage
    stage = 1
    # the environments ID
    env_id = ['SuperMarioBros-7-1-v{}'.format(v) for v in range(4)]


class ShouldMakeSuperMarioBros_7_2(ShouldMakeEnv, TestCase):
    # the current world
    world = 7
    # the current stage
    stage = 2
    # the environments ID
    env_id = ['SuperMarioBros-7-2-v{}'.format(v) for v in range(4)]


class ShouldMakeSuperMarioBros_7_3(ShouldMakeEnv, TestCase):
    # the amount of time left
    time = 300
    # the current world
    world = 7
    # the current stage
    stage = 3
    # the environments ID
    env_id = ['SuperMarioBros-7-3-v{}'.format(v) for v in range(4)]


class ShouldMakeSuperMarioBros_7_4(ShouldMakeEnv, TestCase):
    # the current world
    world = 7
    # the current stage
    stage = 4
    # the environments ID
    env_id = ['SuperMarioBros-7-4-v{}'.format(v) for v in range(4)]


class ShouldMakeSuperMarioBros_8_1(ShouldMakeEnv, TestCase):
    # the amount of time left
    time = 300
    # the current world
    world = 8
    # the current stage
    stage = 1
    # the environments ID
    env_id = ['SuperMarioBros-8-1-v{}'.format(v) for v in range(4)]


class ShouldMakeSuperMarioBros_8_2(ShouldMakeEnv, TestCase):
    # the current world
    world = 8
    # the current stage
    stage = 2
    # the environments ID
    env_id = ['SuperMarioBros-8-2-v{}'.format(v) for v in range(4)]


class ShouldMakeSuperMarioBros_8_3(ShouldMakeEnv, TestCase):
    # the amount of time left
    time = 300
    # the current world
    world = 8
    # the current stage
    stage = 3
    # the environments ID
    env_id = ['SuperMarioBros-8-3-v{}'.format(v) for v in range(4)]


class ShouldMakeSuperMarioBros_8_4(ShouldMakeEnv, TestCase):
    # the current world
    world = 8
    # the current stage
    stage = 4
    # the environments ID
    env_id = ['SuperMarioBros-8-4-v{}'.format(v) for v in range(4)]


class ShouldMakeSuperMarioBrosRandomStagesSubset(ShouldMakeEnv, TestCase):
    # the random number seed for this environment
    seed = 1
    # the amount of time left
    time = 400
    # the current world
    world = 4
    # the current stage
    stage = 2
    # the stages to sample from
    stages = ['4-2']
    # the environments ID for all versions of Super Mario Bros
    env_id = ['SuperMarioBrosRandomStages-v{}'.format(v) for v in range(4)]
