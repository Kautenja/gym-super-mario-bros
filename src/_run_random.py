"""A simple script for debugging the Super Mario Bros. Lua code."""
import gym
import nesgym


if __name__ == "__main__":
    env = gym.make('nesgym/SuperMarioBros-v0')

    done = True
    while True:
        if done:
            state = env.reset()
            done = False
        state, reward, done, info = env.step(4)
        print(reward)
        env.render(mode='rgb_array')
