"""Registration code of Gym environments in this package."""
import math
import gym
from .smb_env import SuperMarioBrosEnv


def _register_mario_env(id: str, **kwargs: dict) -> None:
    """
    Register a Super Mario Bros. (1/2) environment with OpenAI Gym.

    Args:
        id: the id for the env to register
        kwargs: the keyword arguments for the SuperMarioBrosEnv initializer

    Returns:
        None

    """
    gym.envs.registration.register(
        id=id,
        entry_point='gym_super_mario_bros:SuperMarioBrosEnv',
        max_episode_steps=9999999,
        reward_threshold=32000,
        kwargs={ 'max_episode_steps': math.inf, **kwargs},
        nondeterministic=True,
    )


# Super Mario Bros. with standard frame skip
_register_mario_env('SuperMarioBros-v0', frame_skip=4)
_register_mario_env('SuperMarioBros-v1', frame_skip=4, rom_mode='downsample')
_register_mario_env('SuperMarioBros-v2', frame_skip=4, rom_mode='pixel')
_register_mario_env('SuperMarioBros-v3', frame_skip=4, rom_mode='rectangle')


# Super Mario Bros. with no frame skip
_register_mario_env('SuperMarioBrosNoFrameskip-v0', frame_skip=1)
_register_mario_env('SuperMarioBrosNoFrameskip-v1', frame_skip=1, rom_mode='downsample')
_register_mario_env('SuperMarioBrosNoFrameskip-v2', frame_skip=1, rom_mode='pixel')
_register_mario_env('SuperMarioBrosNoFrameskip-v3', frame_skip=1, rom_mode='rectangle')


# Super Mario Bros. 2 (Lost Levels) with standard frame skip
_register_mario_env('SuperMarioBros2-v0', lost_levels=True, frame_skip=4)
_register_mario_env('SuperMarioBros2-v1', lost_levels=True, frame_skip=4, rom_mode='downsample')


# Super Mario Bros. 2 (Lost Levels) with no frame skip
_register_mario_env('SuperMarioBros2NoFrameskip-v0', lost_levels=True, frame_skip=1)
_register_mario_env('SuperMarioBros2NoFrameskip-v1', lost_levels=True, frame_skip=1, rom_mode='downsample')


def make(environment: str) -> gym.Env:
    """Make the environment and return it. same as `gym.make`."""
    return gym.make(environment)


# define the outward facing API of this module (none, gym provides the API)
__all__ = [make.__name__]
