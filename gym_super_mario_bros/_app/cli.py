"""Super Mario Bros for OpenAI Gym."""
import os
import argparse
from .play import play_human, play_random


# The play modes for the system
_PLAY_MODES = {
    'human': play_human,
    'random': play_random
}


def _get_args() -> argparse.ArgumentParser:
    """Create and return an argument parser for this command line interface."""
    parser = argparse.ArgumentParser(description=__doc__)
    # add the argument for the Super Mario Bros environment to run
    parser.add_argument('--env', '-e',
        type=str,
        default='SuperMarioBros-v0',
        help='The name of the environment to play.'
    )
    # add the argument for the mode of execution as either human or random
    parser.add_argument('--mode', '-m',
        type=str,
        default='human',
        choices=['human', 'random'],
        help='The execution mode for the emulation.'
    )
    # add a flag for wrapping the environment
    parser.add_argument('--wrap', '-W',
        action='store_true',
        help='A flag to use the standard wrap while playing.'
    )

    return parser.parse_args()


def main() -> None:
    """The main entry point for the command line interface."""
    # parse arguments from the command line (argparse validates arguments)
    args = _get_args()
    # build the environment with the given ID
    env = make(args.env)
    # wrap the environment if specified
    if args.wrap:
        env = wrap(env, agent_history_length=None)
    # play the environment with the given mode
    _PLAY_MODES[args.mode](env)


# explicitly define the outward facing API of this module
__all__ = [main.__name__]
