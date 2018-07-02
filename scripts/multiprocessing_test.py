"""Test that the multiprocessing package works with the env."""
from multiprocessing import Process
import gym
import base
import gym_super_mario_bros


def play_random() -> None:
    """
    Play the environment making uniformly random decisions.

    Args:
        env: the initialized gym environment to play

    Returns:
        None
    """
    env = gym_super_mario_bros.make('SuperMarioBros-1-1-v0')
    try:
        done = True
        for step in range(500):
            if done:
                state = env.reset()
            action = env.action_space.sample()
            state, reward, done, info = env.step(action)
    except KeyboardInterrupt:
        pass
    # reset and close the environment
    env.reset()
    env.close()



num_procs = 4
procs = [None] * num_procs


for idx in range(num_procs):
    procs[idx] = Process(target=play_random)
    procs[idx].start()
