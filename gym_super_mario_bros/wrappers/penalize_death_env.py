"""A gym wrapper for penalizing deaths."""
import gym
import numpy as np


class PenalizeDeathEnv(gym.Wrapper):
    """a wrapper that penalizes deaths, without terminating episodes."""

    def __init__(self, env: gym.Env, penalty: int=-15) -> None:
        """
        Initialize a new death penalizing environment wrapper.

        Args:
            env: the environment to wrap
            penalty: the penalty for losing a life

        Returns:
            None

        """
        super().__init__(env)
        self.penalty = penalty

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
        obs, reward, done, info = self.env.step(action)
        # update the reward based on the done flag
        reward = self.penalty if done else reward

        return obs, reward, done, info

    def reset(self) -> np.ndarray:
        """Reset the emulator and return the initial state."""
        return self.env.reset()


# explicitly specify the external API of this module
__all__ = [PenalizeDeathEnv.__name__]
