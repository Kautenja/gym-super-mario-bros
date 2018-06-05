"""Methods for playing the game randomly, or as a human."""
import gym
from tqdm import tqdm


def play_human(env: gym.Env) -> None:
    """"""
    pass


def play_random(env: gym.Env) -> None:
    """Play the environment making purely random decisions."""
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

    env.reset()
    env.close()


# explicitly define the outward facing API of this module
__all__ = [
    play_human.__name__,
    play_random.__name__,
]
