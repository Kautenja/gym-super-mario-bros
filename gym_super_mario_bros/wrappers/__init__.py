"""Wrappers for altering the functionality of the game."""
import gym
from .clip_reward_env import ClipRewardEnv
from .downsample_env import DownsampleEnv
from .frame_stack_env import FrameStackEnv
from .monitor import Monitor
from .penalize_death_env import PenalizeDeathEnv
from .reward_cache_env import RewardCacheEnv


def wrap(env: gym.Env,
    image_size: tuple=(84, 84),
    death_penalty: int=-100,
    clip_rewards: bool=False,
    agent_history_length: int=4
) -> gym.Env:
    """
    Wrap an environment with standard wrappers.

    Args:
        env: the environment to wrap
        image_size: the size to down-sample images to
        death_penatly: the penalty for losing a life in a game
        clip_rewards: whether to clip rewards in {-1, 0, +1}
        agent_history_length: the size of the frame buffer for the agent

    Returns:
        a gym environment configured for this experiment

    """
    # wrap the environment with a reward cacher
    env = RewardCacheEnv(env)
    # apply a down-sampler for the given game
    env = DownsampleEnv(env, image_size)
    # apply the death penalty feature if enabled
    if death_penalty is not None:
        env = PenalizeDeathEnv(env, penalty=death_penalty)
    # clip the rewards in {-1, 0, +1} if the feature is enabled
    if clip_rewards:
        env = ClipRewardEnv(env)
    # apply the back history of frames if the feature is enabled
    if agent_history_length is not None:
        env = FrameStackEnv(env, agent_history_length)

    return env


# explicitly define the outward facing API of this package
__all__ = [
    ClipRewardEnv.__name__,
    DownsampleEnv.__name__,
    FrameStackEnv.__name__,
    Monitor.__name__,
    PenalizeDeathEnv.__name__,
    RewardCacheEnv.__name__,
    wrap.__name__,
]
