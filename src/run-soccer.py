import os
from collections import deque

import gym
from gym import wrappers
import nesgym
import numpy as np

from dqn.model import DoubleDQN
from dqn.utils import PiecewiseSchedule


def get_env():
    env = gym.make('nesgym/NekketsuSoccerPK-v0')
    env = nesgym.wrap_nes_env(env)
    expt_dir = '/tmp/soccer/'
    env = wrappers.Monitor(env, os.path.join(expt_dir, "gym"), force=True)
    return env


def soccer_main():
    env = get_env()

    last_obs = env.reset()

    max_timesteps = 40000000

    exploration_schedule = PiecewiseSchedule(
        [
            (0, 1.0),
            (1e5, 0.1),
            (max_timesteps / 2, 0.01),
        ], outside_value=0.01
    )

    dqn = DoubleDQN(image_shape=(84, 84, 1),
                    num_actions=env.action_space.n,
                    training_starts=10000,
                    target_update_freq=4000,
                    training_batch_size=64,
                    # training_starts=1000,
                    # target_update_freq=500,
                    # training_batch_size=3,
                    exploration=exploration_schedule
                   )

    reward_sum_episode = 0
    num_episodes = 0
    episode_rewards = deque(maxlen=100)
    for step in range(max_timesteps):
        if step > 0 and step % 500 == 0:
            print('step: ', step, 'episodes:', num_episodes, 'epsilon:', exploration_schedule.value(step),
                  'learning rate:', dqn.get_learning_rate(), 'last 100 training loss mean', dqn.get_avg_loss(),
                  'last 100 episode mean rewards: ', np.mean(np.array(episode_rewards, dtype=np.float32)))
        # env.render()
        action = dqn.choose_action(step, last_obs)
        obs, reward, done, info = env.step(action)
        reward_sum_episode += reward
        dqn.learn(step, action, reward, done, info)
        if done:
            last_obs = env.reset()
            episode_rewards.append(reward_sum_episode)
            reward_sum_episode = 0
            num_episodes += 1
        else:
            last_obs = obs

if __name__ == "__main__":
    soccer_main()
