"""A gym wrapper for penalizing deaths."""
import gym


class PenalizeDeathEnv(gym.Wrapper):
    """a wrapper that penalizes deaths, without terminating episodes."""

    def __init__(self, env, penalty: int=-1) -> None:
        """
        Initialize a new death penalizing environment wrapper.

        Args:
            env: the environment to wrap
            penalty: the penalty for losing a life

        Returns:
            None

        """
        gym.Wrapper.__init__(self, env)
        self.penalty = penalty

    def step(self, action):
        obs, reward, done, info = self.env.step(action)
        reward = self.penalty if done else reward

        return obs, reward, done, info

    def reset(self):
        return self.env.reset()


# explicitly specify the external API of this module
__all__ = [PenalizeDeathEnv.__name__]
