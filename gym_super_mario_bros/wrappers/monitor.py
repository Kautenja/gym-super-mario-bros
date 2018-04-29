"""A monitor for capturing experiences from game-play."""
import os
from datetime import datetime
import gym
import cv2


def write_video(frames: list, file_path: str, fps: int) -> None:
    """
    Write a video to disk.

    Args:
        frames: a list of numpy frames of the same shape representing frames
        file_path: the path of the file to create

    Returns:
        None

    """
    # cant write an empty video
    if len(frames) == 0:
        return
    # setup a new video writer with cv2
    height, width, channels = frames[0].shape
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(file_path, fourcc, fps, (width, height))
    # write the frames to the video file
    for frame in frames:
        # cv2 wants BGR for some reason?
        video.write(frame[:, :, ::-1])
    # cleanup
    video.release()
    cv2.destroyAllWindows()


class Monitor(gym.Wrapper):
    """A monitor for capturing experiences from game-play."""

    def __init__(self, env, out_dir: str) -> None:
        """
        Initialize a new monitor around an existing environment.

        Args:
            env: the environment to capture game-play from
            out_dir: the directory to write monitoring results to

        Returns:
            None

        """
        super().__init__(env)
        self.out_dir = out_dir
        self.episode = -1
        # setup the timestamped output directory
        now = datetime.today().strftime('%Y-%m-%d_%H-%M-%S')
        self.stamped_out_dir = '{}/{}'.format(self.out_dir, now)
        if not os.path.exists(self.stamped_out_dir):
            os.makedirs(self.stamped_out_dir)
        self.frames = None

    @property
    def current_video_path(self) -> str:
        """Return the path to the current video file."""
        return '{}/{}.mp4'.format(self.stamped_out_dir, self.episode)

    def reset(self) -> any:
        """Reset the environment and return the initial observation."""
        self.episode += 1
        # self.frames is None before the first episode
        if self.frames is not None:
            write_video(
                self.frames,
                self.current_video_path,
                self.env.unwrapped.metadata['video.frames_per_second']
            )
        observation = self.env.reset()
        self.frames = [observation]

        return observation

    def step(self, action: any) -> tuple:
        """
        Take a step using the given action.

        Args:
            action: the action to perform

        Returns:
            a tuple of:
            -   the observation as a result of the action
            -   the reward achieved by taking the action
            -   a flag denoting whether the episode has ended
            -   a dictionary of additional information

        """
        observation, reward, done, info = self.env.step(action)
        self.frames.append(observation)

        return observation, reward, done, info


__all__ = [Monitor.__name__]
