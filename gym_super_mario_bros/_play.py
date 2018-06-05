"""Methods for playing the game randomly, or as a human."""
from tqdm import tqdm
import gym
from ._human_play import play


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
        play(env)
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
        for step in progress:
            if done:
                state = env.reset()
            action = env.action_space.sample()
            state, reward, done, info = env.step(action)
            progress.set_postfix(reward=reward)
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
