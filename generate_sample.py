"""A simple script for debugging the Super Mario Bros. Lua code."""
import os
import gym
import nesgym_super_mario_bros
from tqdm import tqdm
from PIL import Image


# the output directory to dump the sample to
output_dir = 'sample'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)


try:
    env = gym.make('nesgym/SuperMarioBros-v0')
    done = True
    for step in tqdm(range(2000)):
        if done:
            state = env.reset()
        state, reward, done, info = env.step(4)
        Image.fromarray(state).save('{}/{}.png'.format(output_dir, step))
except KeyboardInterrupt:
    pass


env.close()
