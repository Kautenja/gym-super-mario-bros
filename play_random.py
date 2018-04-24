"""A simple script for debugging the Super Mario Bros. Lua code."""
import gym
from tqdm import tqdm
# the package needs imported to register the environment with OpenAI Gym
import nesgym_super_mario_bros


def play_game(env, episodes: int=5000):
    """Play the game."""
    done = True
    for step in tqdm(range(episodes)):
        if done:
            state = env.reset()
        state, reward, done, info = env.step(env.action_space.sample())

    env.close()


try:
    env = gym.make('nesgym/SuperMarioBros-v0')
    play_game(env)
except KeyboardInterrupt:
    env.close()
