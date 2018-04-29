"""A simple script for debugging the Super Mario Bros. Lua code."""
from tqdm import tqdm
import gym_super_mario_bros
from gym_super_mario_bros.wrappers import Monitor


env = gym_super_mario_bros.make('SuperMarioBros-v1')
env = Monitor(env, './monitor')


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
