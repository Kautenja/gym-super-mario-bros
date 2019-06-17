from gym_super_mario_bros import SuperMarioBrosEnv
import tqdm
env = SuperMarioBrosEnv()

done = True

try:
    for _ in tqdm.tqdm(range(5000)):
        if done:
            state = env.reset()
            done = False
        else:
            state, reward, done, info = env.step(env.action_space.sample())
except KeyboardInterrupt:
    pass
