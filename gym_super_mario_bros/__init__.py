"""Registration code of Gym environments in this package."""
from gym.envs.registration import register
from .nesenv import NESEnv
from .smb_env import SuperMarioBrosEnv
import math


# register the environment subclasses with Open.ai Gym
register(
    id='SuperMarioBros-v0',
    entry_point='gym_super_mario_bros:SuperMarioBrosEnv',
    max_episode_steps=9999999,
    reward_threshold=32000,
    kwargs={ 'max_episode_steps': math.inf, 'frame_skip': 4 },
    nondeterministic=True,
)

# register the environment subclasses with Open.ai Gym
register(
    id='SuperMarioBrosNoFrameskip-v0',
    entry_point='gym_super_mario_bros:SuperMarioBrosEnv',
    max_episode_steps=9999999,
    reward_threshold=32000,
    kwargs={ 'max_episode_steps': math.inf, 'frame_skip': 1 },
    nondeterministic=True,
)


# define the outward facing API of this module (none, gym provides the API)
__all__ = []
