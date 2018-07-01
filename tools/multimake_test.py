import gym_super_mario_bros
import multiprocessing as mp


class Env(object):
    def __init__(self, env):
        self.env = env
        self.env.reset()
        self.done = False

    def run(self):
        for step in range(5000):
            if self.done:
                state = self.env.reset()
                self.done = False
            state, reward, self.done, info = self.env.step(self.env.action_space.sample())


def runner(env):
    env.run()


envs = [Env(gym_super_mario_bros.make('SuperMarioBros-v0')) for i in range(4)]
procs = []

for env in envs:
    proc = mp.Process(target=runner, args=(env,))
    proc.start()
    procs.append(proc)

for proc in procs:
    proc.join()
