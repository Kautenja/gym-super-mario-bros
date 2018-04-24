import os
from gym.envs.registration import register
from .nesenv import NESEnv
from .nekketsu_soccer_env import NekketsuSoccerPKEnv
from .smb_env import SuperMarioBrosEnv
from .wrappers import wrap_nes_env

register(
    id='nesgym/NekketsuSoccerPK-v0',
    entry_point='nesgym:NekketsuSoccerPKEnv',
    max_episode_steps=9999999,
    reward_threshold=32000,
    kwargs={},
    nondeterministic=True,
)

register(
    id='nesgym/SuperMarioBros-v0',
    entry_point='nesgym:SuperMarioBrosEnv',
    max_episode_steps=9999999,
    reward_threshold=32000,
    kwargs={},
    nondeterministic=True,
)
