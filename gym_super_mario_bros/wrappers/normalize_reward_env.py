"""An environment wrapper to normalize rewards."""
import gym
import numpy as np


class NormalizeRewardEnv(gym.RewardWrapper):
    """An environment that normalizes rewards about an L infinity norm."""

    def __init__(self, env: gym.Env) -> None:
        """
        Initialize a new reward clipping environment.

        Args:
            env: the environment to wrap

        Returns:
            None

        """
        super().__init__(env)
        self._l_inf_norm = max([abs(r) for r in env.reward_range])
        if self._l_inf_norm == float('inf'):
            raise ValueError('cant normalize a reward with infinite range')

    def reward(self, reward: float) -> float:
        """Normalize the reward."""
        return reward / self._l_inf_norm


# explicitly specify the external API of this module
__all__ = [NormalizeRewardEnv.__name__]
