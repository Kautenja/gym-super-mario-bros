"""Registration code of Gym environments in this package."""
from gym.envs.registration import register
from .nesenv import NESEnv
from .smb_env import SuperMarioBrosEnv


register(
    id='nesgym/SuperMarioBros-v0',
    entry_point='nesgym:SuperMarioBrosEnv',
    max_episode_steps=9999999,
    reward_threshold=32000,
    kwargs={},
    nondeterministic=True,
)


# define the outward facing API of this module (none, gym provides the API)
__all__ = []
