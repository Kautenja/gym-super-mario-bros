"""A simple script for debugging the Super Mario Bros. Lua code."""
import gym
from tqdm import tqdm
import nesgym_super_mario_bros


def play_game(env):
    """Play the game."""
    done = True
    for step in tqdm(range(5000)):
        if done:
            state = env.reset()
        state, reward, done, info = env.step(env.action_space.sample())

    env.close()


try:
    env = gym.make('nesgym/SuperMarioBros-v0')
    play_game(env)
except KeyboardInterrupt:
    env.close()
