"""A script to play the environment with a keyboard."""
import os
from PIL import Image
from datetime import datetime
from gym.utils.play import play
import gym_super_mario_bros


# return a sorted tuple instead of a sorted list
sorted_tuple = lambda x: tuple(sorted(x))


output_dir = 'play'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)


def callback(s, s2, a, r, d, i) -> None:
    """
    Respond to the step callback in the play method.

    Args:
        s: the state before the action was fired
        s2: the state after the action was fired
        a: the action to fire
        r: the reward observed as a result of the action
        d: a flag denoting if the episode is over
        i: the information dictionary from the step

    Returns:
        None

    """
    Image.fromarray(s).save('{}/{}.png'.format(output_dir, datetime.now()))


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


# Create the environment and play the game
env = gym_super_mario_bros.make('SuperMarioBros-v0')
play(env, keys_to_action=keys_to_action, callback=callback)
