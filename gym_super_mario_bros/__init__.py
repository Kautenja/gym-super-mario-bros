"""Registration code of Gym environments in this package."""
import math
import gym
from .smb_env import SuperMarioBrosEnv


# Super Mario Bros with 4 frame skip and no down-sampling
gym.envs.registration.register(
    id='SuperMarioBros-v0',
    entry_point='gym_super_mario_bros:SuperMarioBrosEnv',
    max_episode_steps=9999999,
    reward_threshold=32000,
    kwargs={
        'max_episode_steps': math.inf,
        'frame_skip': 4,
        'lost_levels': False,
        'downsampled_rom': False,
    },
    nondeterministic=True,
)


# Super Mario Bros with 4 frame skip and down-sampling
gym.envs.registration.register(
    id='SuperMarioBros-v1',
    entry_point='gym_super_mario_bros:SuperMarioBrosEnv',
    max_episode_steps=9999999,
    reward_threshold=32000,
    kwargs={
        'max_episode_steps': math.inf,
        'frame_skip': 4,
        'lost_levels': False,
        'downsampled_rom': True,
    },
    nondeterministic=True,
)


# Super Mario Bros with 4 frame skip and pixel ROM Hack
gym.envs.registration.register(
    id='SuperMarioBros-v2',
    entry_point='gym_super_mario_bros:SuperMarioBrosEnv',
    max_episode_steps=9999999,
    reward_threshold=32000,
    kwargs={
        'max_episode_steps': math.inf,
        'frame_skip': 4,
        'lost_levels': False,
        'pixel_rom': True,
    },
    nondeterministic=True,
)


# Super Mario Bros with 1 frame skip and no down-sampling
gym.envs.registration.register(
    id='SuperMarioBrosNoFrameskip-v0',
    entry_point='gym_super_mario_bros:SuperMarioBrosEnv',
    max_episode_steps=9999999,
    reward_threshold=32000,
    kwargs={
        'max_episode_steps': math.inf,
        'frame_skip': 1,
        'lost_levels': False,
        'downsampled_rom': False,
    },
    nondeterministic=True,
)


# Super Mario Bros with 1 frame skip and down-sampling
gym.envs.registration.register(
    id='SuperMarioBrosNoFrameskip-v1',
    entry_point='gym_super_mario_bros:SuperMarioBrosEnv',
    max_episode_steps=9999999,
    reward_threshold=32000,
    kwargs={
        'max_episode_steps': math.inf,
        'frame_skip': 1,
        'lost_levels': False,
        'downsampled_rom': True,
    },
    nondeterministic=True,
)


# Super Mario Bros with 1 frame skip and pixel ROM Hack
gym.envs.registration.register(
    id='SuperMarioBrosNoFrameskip-v2',
    entry_point='gym_super_mario_bros:SuperMarioBrosEnv',
    max_episode_steps=9999999,
    reward_threshold=32000,
    kwargs={
        'max_episode_steps': math.inf,
        'frame_skip': 1,
        'lost_levels': False,
        'pixel_rom': True,
    },
    nondeterministic=True,
)




# Super Mario Bros 2 with 4 frame skip and no down-sampling
gym.envs.registration.register(
    id='SuperMarioBros2-v0',
    entry_point='gym_super_mario_bros:SuperMarioBrosEnv',
    max_episode_steps=9999999,
    reward_threshold=32000,
    kwargs={
        'max_episode_steps': math.inf,
        'frame_skip': 4,
        'lost_levels': True,
        'downsampled_rom': False,
    },
    nondeterministic=True,
)


# Super Mario Bros 2 with 4 frame skip and down-sampling
gym.envs.registration.register(
    id='SuperMarioBros2-v1',
    entry_point='gym_super_mario_bros:SuperMarioBrosEnv',
    max_episode_steps=9999999,
    reward_threshold=32000,
    kwargs={
        'max_episode_steps': math.inf,
        'frame_skip': 4,
        'lost_levels': True,
        'downsampled_rom': True,
    },
    nondeterministic=True,
)


# Super Mario Bros 2 with 1 frame skip and no down-sampling
gym.envs.registration.register(
    id='SuperMarioBros2NoFrameskip-v0',
    entry_point='gym_super_mario_bros:SuperMarioBrosEnv',
    max_episode_steps=9999999,
    reward_threshold=32000,
    kwargs={
        'max_episode_steps': math.inf,
        'frame_skip': 1,
        'lost_levels': True,
        'downsampled_rom': False,
    },
    nondeterministic=True,
)


# Super Mario Bros 2 with 1 frame skip and down-sampling
gym.envs.registration.register(
    id='SuperMarioBros2NoFrameskip-v1',
    entry_point='gym_super_mario_bros:SuperMarioBrosEnv',
    max_episode_steps=9999999,
    reward_threshold=32000,
    kwargs={
        'max_episode_steps': math.inf,
        'frame_skip': 1,
        'lost_levels': True,
        'downsampled_rom': True,
    },
    nondeterministic=True,
)


def make(environment: str) -> gym.Env:
    """Make the environment and return it. same as `gym.make`."""
    return gym.make(environment)


# define the outward facing API of this module (none, gym provides the API)
__all__ = [make.__name__]
