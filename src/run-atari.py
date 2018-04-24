import gym
import numpy as np

from dqn.model import DoubleDQN
from dqn.atari_wrappers import wrap_deepmind
from dqn.utils import PiecewiseSchedule

from collections import deque

def get_env(task, seed):
    env_id = task.env_id
    env = gym.make(env_id)
    env.seed(seed)

    env = wrap_deepmind(env)

    return env


def atari_main():
    # Get Atari games.
    benchmark = gym.benchmark_spec('Atari40M')

    # Change the index to select a different game.
    # ['BeamRiderNoFrameskip-v4', 'BreakoutNoFrameskip-v4', 'EnduroNoFrameskip-v4',
    #  'PongNoFrameskip-v4', 'QbertNoFrameskip-v4', 'SeaquestNoFrameskip-v4',
    #  'SpaceInvadersNoFrameskip-v4']
    task = benchmark.tasks[1]

    print('availabe tasks: ', [t.env_id for t in benchmark.tasks])
    print('task: ', task.env_id, 'max steps: ', task.max_timesteps)

    # Run training
    seed = 0 # Use a seed of zero (you may want to randomize the seed!)
    env = get_env(task, seed)

    last_obs = env.reset()

    exploration_schedule = PiecewiseSchedule(
        [
            (0, 1.0),
            (1e6, 0.1),
            (task.max_timesteps / 2, 0.01),
        ], outside_value=0.01
    )

    dqn = DoubleDQN(image_shape=(84, 84, 1),
                    num_actions=env.action_space.n,
                    training_starts=50000,
                    target_update_freq=10000,
                    training_batch_size=32,
                    # training_starts=2000,
                    # target_update_freq=500,
                    # training_batch_size=3,
                    exploration=exploration_schedule
                   )

    reward_sum_episode = 0
    num_episodes = 0
    episode_rewards = deque(maxlen=100)
    for step in range(task.max_timesteps):
        if step > 0 and step % 1000 == 0:
            print('step: ', step, 'episodes:', num_episodes, 'epsilon:', exploration_schedule.value(step),
                  'learning rate:', dqn.get_learning_rate(), 'last 100 training loss mean', dqn.get_avg_loss(),
                  'last 100 episode mean rewards: ', np.mean(np.array(episode_rewards, dtype=np.float32)))
        env.render()
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
    atari_main()
