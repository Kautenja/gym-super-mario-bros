"""An environment wrapper to clip rewards."""
import gym
import numpy as np


class ClipRewardEnv(gym.RewardWrapper):
    """An environment that clips rewards in {-1, 0, 1}."""

    def __init__(self, env):
        """Initialize a new reward clipping environment."""
        gym.RewardWrapper.__init__(self, env)

    def reward(self, reward):
        """Bin reward to {-1, 0, +1} using its sign."""
        return np.sign(reward)


# explicitly specify the external API of this module
__all__ = [ClipRewardEnv.__name__]
