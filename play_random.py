"""A simple script for debugging the Super Mario Bros. Lua code."""
from tqdm import tqdm
import gym
import gym_super_mario_bros


env = gym.make('SuperMarioBros-v0')


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


env.close()
