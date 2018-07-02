"""A gym wrapper for caching rewards."""
import gym
import numpy as np


class RewardCacheEnv(gym.Wrapper):
    """a wrapper that caches rewards of episodes."""

    def __init__(self, env) -> None:
        """
        Initialize a reward caching environment.

        Args:
            env: the environment to wrap

        Returns:
            None

        """
        super().__init__(env)
        self._score = 0
        self.env.unwrapped.episode_rewards = []

    def step(self, action: any) -> tuple:
        """
        Take a step using the given action.

        Args:
            action: the discrete action to perform.

        Returns:
            a tuple of:
            -   the start as a result of the action
            -   the reward achieved by taking the action
            -   a flag denoting whether the episode has ended
            -   a dictionary of extra information

        """
        state, reward, done, info = self.env.step(action)
        self._score += reward
        if done:
            self.env.unwrapped.episode_rewards.append(self._score)
            self._score = 0
        return state, reward, done, info

    def reset(self) -> np.ndarray:
        """Reset the emulator and return the initial state."""
        return self.env.reset()


# explicitly specify the external API of this module
__all__ = [RewardCacheEnv.__name__]
