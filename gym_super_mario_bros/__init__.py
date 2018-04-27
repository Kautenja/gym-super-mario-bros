"""Registration code of Gym environments in this package."""
import math
import gym
from .smb_env import SuperMarioBrosEnv


# register the environment subclasses with Open.ai Gym
gym.envs.registration.register(
    id='SuperMarioBros-v0',
    entry_point='gym_super_mario_bros:SuperMarioBrosEnv',
    max_episode_steps=9999999,
    reward_threshold=32000,
    kwargs={ 'max_episode_steps': math.inf, 'frame_skip': 4 },
    nondeterministic=True,
)

# register the environment subclasses with Open.ai Gym
gym.envs.registration.register(
    id='SuperMarioBrosNoFrameskip-v0',
    entry_point='gym_super_mario_bros:SuperMarioBrosEnv',
    max_episode_steps=9999999,
    reward_threshold=32000,
    kwargs={ 'max_episode_steps': math.inf, 'frame_skip': 1 },
    nondeterministic=True,
)


def make(environment: str) -> 'Environment':
    """Make the environment and return it. same as `gym.make`."""
    return gym.make(environment)


# define the outward facing API of this module (none, gym provides the API)
__all__ = []
