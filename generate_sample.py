"""A simple script to generate output from the emulator for debugging."""
import os
from tqdm import tqdm
from PIL import Image
import gym
import nesgym_super_mario_bros


# the output directory to dump the sample to
output_dir = 'sample'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)


try:
    env = gym.make('nesgym/SuperMarioBros-v0')

    for t in tqdm(range(5)):
        state = env.reset()
        Image.fromarray(state).save('{}/{}_0.png'.format(output_dir, t))
        frames = 0
        done = False
        while not done:
            state, _, done, _ = env.step(4)
            frames += 1
            Image.fromarray(state).save('{}/{}_{}.png'.format(output_dir, t, frames))

except KeyboardInterrupt:
    pass


env.close()
