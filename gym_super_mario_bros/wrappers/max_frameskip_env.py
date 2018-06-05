"""An environment to skip k frames and return a max between the last two."""
import gym
import numpy as np


class MaxFrameskipEnv(gym.Wrapper):
    """An environment to skip k frames and return a max between the last two."""

    def __init__(self, env, skip: int=4) -> None:
        """
        Initialize a new max frame skip env around an existing environment.

        Args:
            env: the environment to wrap around
            skip: the number of frames to skip (i.e. hold an action for)

        Returns:
            None

        """
        gym.Wrapper.__init__(self, env)
        # most recent raw observations (for max pooling across time steps)
        self._obs_buffer = np.zeros((2, *env.observation_space.shape), dtype=np.uint8)
        self._skip = skip

    def step(self, action):
        """Repeat action, sum reward, and max over last observations."""
        # the total reward from `skip` frames having `action` held on them
        total_reward = 0.0
        done = None
        # perform the action `skip` times
        for i in range(self._skip):
            obs, reward, done, info = self.env.step(action)
            total_reward += reward
            # assign the buffer with the last two frames
            if i == self._skip - 2:
                self._obs_buffer[0] = obs
            if i == self._skip - 1:
                self._obs_buffer[1] = obs
            # break the loop if the game terminated
            if done:
                break
        # Note that the observation on the done=True frame doesn't matter
        # (because the next state isn't evaluated when done is true)
        max_frame = self._obs_buffer.max(axis=0)

        return max_frame, total_reward, done, info

    def reset(self, **kwargs):
        return self.env.reset(**kwargs)


# explicitly define the outward facing API of this module
__all__ = [MaxFrameskipEnv.__name__]
