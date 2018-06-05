"""Super Mario Bros for OpenAI Gym."""
import argparse
from ._registration import make
from .wrappers import wrap


def create_argparser() -> argparse.ArgumentParser:
    """Create and return an argument parser for this command line interface."""
    parser = argparse.ArgumentParser(description=__doc__)
    # add the argument for the Super Mario Bros environment to run
    parser.add_argument('--env', '-e',
        type=str,
        default='SuperMarioBros-v0',
        choices=[
            'SuperMarioBros-v0',
            'SuperMarioBros-v1',
            'SuperMarioBros-v2',
            'SuperMarioBros-v3',
            'SuperMarioBrosNoFrameskip-v0',
            'SuperMarioBrosNoFrameskip-v1',
            'SuperMarioBrosNoFrameskip-v2',
            'SuperMarioBrosNoFrameskip-v3',
            'SuperMarioBros2-v0',
            'SuperMarioBros2-v1',
            'SuperMarioBros2NoFrameskip-v0',
            'SuperMarioBros2NoFrameskip-v1',
        ],
        help='The name of the environment to play.'
    )
    # add the argument for the mode of execution as either human or random
    parser.add_argument('--mode', '-m',
        type=str,
        default='human',
        choices=['human', 'random'],
        help='The execution mode as either `human` or `random`.'
    )

    return parser


def main() -> None:
    """The main entry point for the command line interface."""
    args = create_argparser().parse_args()
    env_name = args.env
    mode = args.mode

    print(env_name)
    print(mode)
