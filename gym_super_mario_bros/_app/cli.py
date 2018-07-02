"""Super Mario Bros for OpenAI Gym."""
import os
import argparse
from .._registration import make
from ..wrappers import wrap
from .play import play_human, play_random


def create_argparser() -> argparse.ArgumentParser:
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

    return parser


def main() -> None:
    """The main entry point for the command line interface."""
    # parse arguments from the command line (argparse validates arguments)
    args = create_argparser().parse_args()
    # select the method for playing the game
    if args.mode == 'human':
        os.environ['HUMAN_PLAY'] = str(True)
        play = play_human
    elif args.mode == 'random':
        play = play_random
    # play the game
    env = make(args.env)
    # wrap the environment if specified
    if args.wrap:
        env = wrap(env, agent_history_length=None)
    play(env)


# explicitly define the outward facing API of this module
__all__ = [main.__name__]
