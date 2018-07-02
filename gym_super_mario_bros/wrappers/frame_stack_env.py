"""An environment wrapper to stack observations into a tensor."""
from collections import deque
import gym
import numpy as np
from ._util import LazyFrames


class FrameStackEnv(gym.Wrapper):
    """An environment wrapper to stack observations into a tensor."""

    def __init__(self, env: gym.Env, k: int) -> None:
        """
        Initialize a wrapper to stack the last k frames.

        Args:
            env: the environment to wrap
            k: the number of previous frames to stack together

        Returns:
            None

        """
        super().__init__(env)
        self.k = k
        self.frames = deque([], maxlen=k)
        # setup the new observation space based on the k frame skip
        shp = env.observation_space.shape
        self.observation_space = gym.spaces.Box(
            low=0,
            high=255,
            shape=(shp[0], shp[1], shp[2] * k),
            dtype=np.uint8
        )

    def _get_ob(self) -> LazyFrames:
        """Return a LazyFrames object of the stack of frame."""
        assert len(self.frames) == self.k
        return LazyFrames(list(self.frames))

    def reset(self) -> LazyFrames:
        """Reset the emulator and return the initial state."""
        ob = self.env.reset()
        for _ in range(self.k):
            self.frames.append(ob)

        return self._get_ob()

    def step(self, action: int) -> tuple:
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
        frame, reward, done, info = self.env.step(action)
        # add the frame to the queue
        self.frames.append(frame)

        return self._get_ob(), reward, done, info


# explicitly define the outward facing API of this module
__all__ = [FrameStackEnv.__name__]
