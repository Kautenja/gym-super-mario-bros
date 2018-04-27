"""Registration code of Gym environments in this package."""
import math
import gym
from .smb_env import SuperMarioBrosEnv


gym.envs.registration.register(
    id='SuperMarioBros-v0',
    entry_point='gym_super_mario_bros:SuperMarioBrosEnv',
    max_episode_steps=9999999,
    reward_threshold=32000,
    kwargs={
        'max_episode_steps': math.inf,
        'frame_skip': 4,
        'downsampled_rom': False,
    },
    nondeterministic=True,
)

gym.envs.registration.register(
    id='SuperMarioBros-v1',
    entry_point='gym_super_mario_bros:SuperMarioBrosEnv',
    max_episode_steps=9999999,
    reward_threshold=32000,
    kwargs={
        'max_episode_steps': math.inf,
        'frame_skip': 4,
        'downsampled_rom': True,
    },
    nondeterministic=True,
)



gym.envs.registration.register(
    id='SuperMarioBrosNoFrameskip-v0',
    entry_point='gym_super_mario_bros:SuperMarioBrosEnv',
    max_episode_steps=9999999,
    reward_threshold=32000,
    kwargs={
        'max_episode_steps': math.inf,
        'frame_skip': 1,
        'downsampled_rom': False,
    },
    nondeterministic=True,
)

gym.envs.registration.register(
    id='SuperMarioBrosNoFrameskip-v1',
    entry_point='gym_super_mario_bros:SuperMarioBrosEnv',
    max_episode_steps=9999999,
    reward_threshold=32000,
    kwargs={
        'max_episode_steps': math.inf,
        'frame_skip': 1,
        'downsampled_rom': True,
    },
    nondeterministic=True,
)



def make(environment: str) -> gym.Env:
    """Make the environment and return it. same as `gym.make`."""
    return gym.make(environment)


# define the outward facing API of this module (none, gym provides the API)
__all__ = [make.__name__]
