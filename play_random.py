"""A simple script for debugging the Super Mario Bros. Lua code."""
import gym
from tqdm import tqdm
# the package needs imported to register the environment with OpenAI Gym
import nesgym_super_mario_bros


def play_game(env, episodes: int=5000):
    """Play the game."""
    done = True
    progress = tqdm(range(episodes))
    for step in progress:
        if done:
            state = env.reset()
        action = env.action_space.sample()
        state, reward, done, info = env.step(action)
        progress.set_postfix(reward=reward)
    env.close()


try:
    env = gym.make('nesgym/SuperMarioBros-v0')
    play_game(env)
except KeyboardInterrupt:
    env.close()
