"""A simple script for debugging the Super Mario Bros. Lua code."""
import gym
import nesgym_super_mario_bros


env = gym.make('nesgym/SuperMarioBros-v0')


done = True
for step in range(5000):
    print(step)
    if done:
        print('done')
        state = env.reset()
    state, reward, done, info = env.step(env.action_space.sample())

env.close()
