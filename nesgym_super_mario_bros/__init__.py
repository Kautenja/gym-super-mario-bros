"""Registration code of Gym environments in this package."""
from gym.envs.registration import register
from .nesenv import NESEnv
from .smb_env import SuperMarioBrosEnv


# the version of the package
__version__ = '0.1.1'
# the URL to find the source code and releases
__url__ = 'https://github.com/Kautenja/nesgym-super-mario-bros'


# register the environment subclasses with Open.ai Gym
register(
    id='nesgym/SuperMarioBros-v0',
    entry_point='nesgym_super_mario_bros:SuperMarioBrosEnv',
    max_episode_steps=9999999,
    reward_threshold=32000,
    kwargs={},
    nondeterministic=True,
)


# define the outward facing API of this module (none, gym provides the API)
__all__ = []
