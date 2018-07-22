"""Methods for playing the game randomly, or as a human."""
from tqdm import tqdm
import gym
from .play_human import play


def play_human(env):
    """
    Play the environment using keyboard as a human.

    Args:
        env (gym.Env): the initialized gym environment to play

    Returns:
        None

    """
    # play the game and catch a potential keyboard interrupt
    try:
        play(env, fps=env.metadata['video.frames_per_second'])
    except KeyboardInterrupt:
        pass
    # reset and close the environment
    env.close()


def play_random(env):
    """
    Play the environment making uniformly random decisions.

    Args:
        env (gym.Env): the initialized gym environment to play

    Returns:
        None

    """
    try:
        done = True
        progress = tqdm(range(5000))
        for _ in progress:
            if done:
                state = env.reset()
            action = env.action_space.sample()
            state, reward, done, _ = env.step(action)
            progress.set_postfix(reward=reward)
            env.render()
    except KeyboardInterrupt:
        pass
    # reset and close the environment
    env.close()


# explicitly define the outward facing API of this module
__all__ = [
    play_human.__name__,
    play_random.__name__,
]
