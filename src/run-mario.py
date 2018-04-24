import os
from collections import deque

import gym
from gym import wrappers
import nesgym
import numpy as np



def get_env():
    env = gym.make('nesgym/SuperMarioBros-v0')
    env = nesgym.wrap_nes_env(env)
    expt_dir = '/tmp/mario/'
    env = wrappers.Monitor(env, os.path.join(expt_dir, "gym"), force=True)
    return env


def mario_main():
    env = get_env()

    last_obs = env.reset()


    done = False
    while True:
        state, reward, done, info = env.step(4)
        env.render(mode='rgb_array')
        if done:
            state = env.reset()


if __name__ == "__main__":
    mario_main()
