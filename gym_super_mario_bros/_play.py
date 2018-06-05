"""Methods for playing the game randomly, or as a human."""
from tqdm import tqdm
import gym
from .human_play import play


def play_human(env: gym.Env) -> None:
    """
    Play the environment using keyboard as a human.

    Args:
        env: the initialized gym environment to play

    Returns:
        None

    """
    # return a sorted tuple instead of a sorted list
    sorted_tuple = lambda x: tuple(sorted(x))
    # Mapping of buttons on the NES joy-pad to keyboard keys
    up =    ord('w')
    down =  ord('s')
    left =  ord('a')
    right = ord('d')
    A =     ord('o')
    B =     ord('p')
    # A mapping of pressed key combinations to discrete actions in action space
    keys_to_action = {
        (): 0,
        (up, ): 1,
        (down, ): 2,
        (left, ): 3,
        (right, ): 4,
        sorted_tuple((left, A, )): 5,
        sorted_tuple((left, B, )): 6,
        sorted_tuple((left, A, B, )): 7,
        sorted_tuple((right, A, )): 8,
        sorted_tuple((right, B, )): 9,
        sorted_tuple((right, A, B, )): 10,
        (A, ): 11,
        (B, ): 12,
        sorted_tuple((A, B)): 13
    }
    # play the game and catch a potential keyboard interrupt
    try:
        play(env, keys_to_action=keys_to_action)
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
