"""Test cases for the command line interface."""
from argparse import Namespace
from contextlib import redirect_stderr
from io import StringIO
from unittest import TestCase
from unittest.mock import patch

from gymnasium import Env

from .._app import cli
from ..actions import SIMPLE_MOVEMENT


class _FakeActionSpace:
    """A minimal deterministic action space for playback tests."""

    def sample(self):
        """Return a fixed action."""
        return 0


class _FakeEnv(Env):
    """A minimal Gymnasium environment for CLI tests."""

    metadata = {'render_fps': 60}
    action_space = _FakeActionSpace()

    def __init__(self):
        """Initialize reset, step, render, and close call tracking."""
        self.reset_calls = []
        self.step_calls = []
        self.render_calls = 0
        self.close_calls = 0

    def reset(self, **kwargs):
        """Record reset calls and return a Gymnasium reset tuple."""
        self.reset_calls.append(kwargs)
        return None, {}

    def step(self, action):
        """Record step calls and return a Gymnasium step tuple."""
        self.step_calls.append(action)
        return None, 1.0, False, False, {}

    def render(self):
        """Record render calls."""
        self.render_calls += 1

    def close(self):
        """Record close calls."""
        self.close_calls += 1


def _parse_error(argv):
    """Parse arguments and return the argparse SystemExit error."""
    with redirect_stderr(StringIO()):
        with TestCase().assertRaises(SystemExit) as error:
            cli._get_args(argv)
    return error.exception


class ShouldParseCliOptions(TestCase):
    """Test cases for CLI argument parsing."""

    def test_human_mode_requires_rendering(self):
        error = _parse_error(['--mode', 'human', '--no-render'])

        self.assertEqual(2, error.code)

    def test_random_mode_requires_positive_steps(self):
        error = _parse_error(['--mode', 'random', '--steps', '0'])

        self.assertEqual(2, error.code)

    def test_stages_are_limited_to_random_stage_envs(self):
        error = _parse_error(['--stages', '1-4'])

        self.assertEqual(2, error.code)

    def test_random_stage_env_accepts_stage_subset(self):
        args = cli._get_args([
            '--env', 'SuperMarioBrosRandomStages-v0',
            '--stages', '1-4', '2-4',
        ])

        self.assertEqual(['1-4', '2-4'], args.stages)


class ShouldBuildCliEnvironment(TestCase):
    """Test cases for creating environments from CLI args."""

    def test_random_no_render_constructs_headless_env(self):
        env = _FakeEnv()

        with patch.object(cli.gym, 'make', return_value=env) as gym_make:
            with patch.object(cli, 'play_random') as play_random:
                cli.main(['--mode', 'random', '--steps', '5', '--no-render'])

        gym_make.assert_called_once_with('SuperMarioBros-v0', render_mode=None)
        play_random.assert_called_once_with(
            env,
            5,
            render=False,
            progress=True,
        )

    def test_random_render_constructs_human_render_env(self):
        env = _FakeEnv()

        with patch.object(cli.gym, 'make', return_value=env) as gym_make:
            with patch.object(cli, 'play_random'):
                cli.main(['--mode', 'random', '--steps', '5'])

        gym_make.assert_called_once_with('SuperMarioBros-v0', render_mode='human')

    def test_actionspace_wraps_with_public_preset(self):
        env = _FakeEnv()
        wrapped = _FakeEnv()

        with patch.object(cli.gym, 'make', return_value=env):
            with patch.object(cli, 'JoypadSpace', return_value=wrapped) as joypad:
                with patch.object(cli, 'play_random') as play_random:
                    cli.main([
                        '--mode', 'random',
                        '--no-render',
                        '--actionspace', 'simple',
                    ])

        joypad.assert_called_once_with(env, SIMPLE_MOVEMENT)
        play_random.assert_called_once_with(
            wrapped,
            500,
            render=False,
            progress=True,
        )

    def test_seed_applies_to_first_playback_reset(self):
        env = _FakeEnv()

        def reset_during_playback(env, *_args, **_kwargs):
            env.reset()
            env.reset()

        with patch.object(cli.gym, 'make', return_value=env):
            with patch.object(cli, 'play_random', side_effect=reset_during_playback):
                cli.main([
                    '--mode', 'random',
                    '--steps', '1',
                    '--no-render',
                    '--seed', '123',
                ])

        self.assertEqual([{'seed': 123}, {}], env.reset_calls)

    def test_random_stage_subset_is_passed_to_env(self):
        env = _FakeEnv()

        with patch.object(cli.gym, 'make', return_value=env) as gym_make:
            with patch.object(cli, 'play_random'):
                cli.main([
                    '--mode', 'random',
                    '--no-render',
                    '--env', 'SuperMarioBrosRandomStages-v0',
                    '--stages', '1-4', '2-4',
                ])

        gym_make.assert_called_once_with(
            'SuperMarioBrosRandomStages-v0',
            render_mode=None,
            stages=['1-4', '2-4'],
        )


class ShouldPlayCliEnvironment(TestCase):
    """Test cases for playback helper behavior."""

    def test_random_no_render_playback_does_not_render_frames(self):
        env = _FakeEnv()
        args = Namespace(
            mode='random',
            steps=3,
            render=False,
            progress=False,
        )

        cli._play(env, args)

        self.assertEqual([{}], env.reset_calls)
        self.assertEqual([0, 0, 0], env.step_calls)
        self.assertEqual(0, env.render_calls)
        self.assertEqual(1, env.close_calls)
