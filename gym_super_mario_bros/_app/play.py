"""Methods for playing the game randomly, or as a human."""
from tqdm import tqdm
import gym
from .play_human import play


def play_human(env: gym.Env) -> None:
    """
    Play the environment using keyboard as a human.

    Args:
        env: the initialized gym environment to play

    Returns:
        None

    """
    # play the game and catch a potential keyboard interrupt
    try:
        play(env, fps=env.metadata['video.frames_per_second'])
    except KeyboardInterrupt:
        pass
    # reset and close the environment
    env.reset()
    env.close()


def play_random(env: gym.Env) -> None:
    """
    Play the environment making uniformly random decisions.

    Args:
        env: the initialized gym environment to play

    Returns:
        None
    """
    try:
        done = True
        progress = tqdm(range(500))
        for _ in progress:
            if done:
                _ = env.reset()
            action = env.action_space.sample()
            _, reward, done, _ = env.step(action)
            progress.set_postfix(reward=reward)
            env.render()
    except KeyboardInterrupt:
        pass
    # reset and close the environment
    env.reset()
    env.close()


# explicitly define the outward facing API of this module
__all__ = [
    play_human.__name__,
    play_random.__name__,
]
