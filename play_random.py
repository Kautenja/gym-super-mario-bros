"""Play a Super Mario Bros environment using uniform random movement.

    python play_random.py <Environment Name>
"""
import sys


try:
    # try to load the environment name from the command line
    env_name = sys.argv[1]
except IndexError:
    # print the script documentation and exit
    print(__doc__)
    sys.exit(-1)


# import these here so command line error handling (above) runs fast
from tqdm import tqdm
import gym_super_mario_bros
from gym_super_mario_bros.wrappers import Monitor


# create the environment and wrap it with a monitor
env = gym_super_mario_bros.make(env_name)
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
