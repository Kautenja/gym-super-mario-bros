"""Super Mario Bros for OpenAI Gym."""
import os
import argparse
from nes_py.wrappers import wrap
from nes_py.wrappers import BinarySpaceToDiscreteSpaceEnv
from nes_py._app.play import play_human, play_random
from .._registration import make
from ..actions import RIGHT_ONLY, SIMPLE_MOVEMENT, COMPLEX_MOVEMENT


# The play modes for the system
_PLAY_MODES = {
    'human': play_human,
    'random': play_random
}


# a key mapping of action spaces to wrap with
_ACTION_SPACES = {
    'right': RIGHT_ONLY,
    'simple': SIMPLE_MOVEMENT,
    'complex': COMPLEX_MOVEMENT,
}


def _get_args():
    """Parse command line arguments and return them."""
    parser = argparse.ArgumentParser(description=__doc__)
    # add the argument for the Super Mario Bros environment to run
    parser.add_argument('--env', '-e',
        type=str,
        default='SuperMarioBros-v0',
        help='The name of the environment to play'
    )
    # add the argument for the mode of execution as either human or random
    parser.add_argument('--mode', '-m',
        type=str,
        default='human',
        choices=['human', 'random'],
        help='The execution mode for the emulation'
    )
    # add a flag for wrapping the environment
    parser.add_argument('--wrap', '-W',
        action='store_true',
        help='A flag to use the standard wrap while playing'
    )
    # add the argument for adjusting the action space
    parser.add_argument('--actionspace', '-a',
        type=str,
        default='nes',
        choices=['nes', 'right', 'simple', 'complex'],
        help='the action space wrapper to use'
    )
    # parse arguments and return them
    return parser.parse_args()


def main():
    """The main entry point for the command line interface."""
    # parse arguments from the command line (argparse validates arguments)
    args = _get_args()
    # build the environment with the given ID
    env = make(args.env)
    # wrap the environment with an action space if specified
    if args.actionspace != 'nes':
        print(args.actionspace)
        # unwrap the actions list by key
        actions = _ACTION_SPACES[args.actionspace]
        # wrap the environment with the new action space
        env = BinarySpaceToDiscreteSpaceEnv(env, actions)
    # wrap the environment if specified
    if args.wrap:
        env = wrap(env, agent_history_length=None)
    # play the environment with the given mode
    _PLAY_MODES[args.mode](env)


# explicitly define the outward facing API of this module
__all__ = [main.__name__]
