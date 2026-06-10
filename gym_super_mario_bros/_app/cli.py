"""Super Mario Bros for Gymnasium."""
import argparse
import sys

import gymnasium as gym
from nes_py.play import play_human
from nes_py.play import play_random
from nes_py.wrappers import JoypadSpace

from ..actions import RIGHT_ONLY, SIMPLE_MOVEMENT, COMPLEX_MOVEMENT


# a key mapping of action spaces to wrap with
_ACTION_SPACES = {
    'right': RIGHT_ONLY,
    'simple': SIMPLE_MOVEMENT,
    'complex': COMPLEX_MOVEMENT,
}


class _FirstResetSeed(gym.Wrapper):
    """Apply a CLI seed to the first reset invoked by nes_py.play."""

    def __init__(self, env, seed):
        """Initialize the wrapper with the given seed."""
        super().__init__(env)
        self._first_reset_seed = seed
        self._seed_is_pending = seed is not None

    def reset(self, **kwargs):
        """Reset the environment, applying the configured seed once."""
        if self._seed_is_pending:
            self._seed_is_pending = False
            if kwargs.get('seed') is None:
                kwargs['seed'] = self._first_reset_seed
        return self.env.reset(**kwargs)


def _parser():
    """Build the command line argument parser."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--env', '-e',
        type=str,
        default='SuperMarioBros-v0',
        help='The name of the environment to play'
    )
    parser.add_argument('--mode', '-m',
        type=str,
        default='human',
        choices=['human', 'random'],
        help='The execution mode for the emulation'
    )
    parser.add_argument('--actionspace', '-a',
        type=str,
        default='nes',
        choices=['nes', 'right', 'simple', 'complex'],
        help='the action space wrapper to use'
    )
    parser.add_argument('--seed',
        type=int,
        help='the seed to use on the first environment reset',
    )
    parser.add_argument('--steps', '-s',
        type=int,
        default=500,
        help='The number of random steps to take.',
    )
    parser.add_argument('--render',
        action=argparse.BooleanOptionalAction,
        default=True,
        help='render frames to a graphical window',
    )
    parser.add_argument('--no-progress',
        action='store_false',
        dest='progress',
        help='disable the random-mode progress bar',
    )
    parser.set_defaults(progress=True)
    return parser


def _get_args(argv=None):
    """Parse command line arguments and return them."""
    parser = _parser()
    # parse arguments and return them
    args = parser.parse_args(argv)
    if args.mode == 'human' and not args.render:
        parser.error('human mode requires graphical rendering')
    if args.mode == 'random' and args.steps <= 0:
        parser.error('--steps must be positive in random mode')
    return args


def _render_mode(args):
    """Return the render mode to use when creating the environment."""
    if args.mode == 'random' and args.render:
        return 'human'
    return None


def _make_env(args):
    """Build and wrap the environment described by args."""
    kwargs = {'render_mode': _render_mode(args)}
    env = gym.make(args.env, **kwargs)
    # wrap the environment with an action space if specified
    if args.actionspace != 'nes':
        # unwrap the actions list by key
        actions = _ACTION_SPACES[args.actionspace]
        # wrap the environment with the new action space
        env = JoypadSpace(env, actions)
    if args.seed is not None:
        env = _FirstResetSeed(env, args.seed)
    return env


def _play(env, args):
    """Play the environment with the requested mode."""
    # play the environment with the given mode
    if args.mode == 'human':
        play_human(env)
    else:
        play_random(
            env,
            args.steps,
            render=args.render,
            progress=args.progress,
        )


def main(argv=None):
    """The main entry point for the command line interface."""
    # parse arguments from the command line (argparse validates arguments)
    args = _get_args(argv)
    # build the environment with the given ID
    env = _make_env(args)
    _play(env, args)
    return 0


# explicitly define the outward facing API of this module
__all__ = [main.__name__]


if __name__ == '__main__':
    sys.exit(main())
