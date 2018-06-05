"""A gym wrapper for caching rewards."""
import gym


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
        gym.Wrapper.__init__(self, env)
        self._score = 0
        self.env.unwrapped.episode_rewards = []

    def step(self, action):
        state, reward, done, info = self.env.step(action)
        self._score += reward
        if done:
            self.env.unwrapped.episode_rewards.append(self._score)
            self._score = 0
        return state, reward, done, info

    def reset(self, **kwargs):
        return self.env.reset(**kwargs)


# explicitly specify the external API of this module
__all__ = [RewardCacheEnv.__name__]
