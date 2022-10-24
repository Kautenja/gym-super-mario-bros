"""An OpenAI Gym Super Mario Bros. environment that randomly selects levels."""
import gym
import numpy as np
from .smb_env import SuperMarioBrosEnv


class SuperMarioBrosRandomStagesEnv(gym.Env):
    """A Super Mario Bros. environment that randomly selects levels."""

    # relevant meta-data about the environment
    metadata = SuperMarioBrosEnv.metadata

    # the legal range of rewards for each step
    reward_range = SuperMarioBrosEnv.reward_range

    # observation space for the environment is static across all instances
    observation_space = SuperMarioBrosEnv.observation_space

    # action space is a bitmap of button press values for the 8 NES buttons
    action_space = SuperMarioBrosEnv.action_space

    def __init__(self, rom_mode='vanilla', stages=None):
        """
        Initialize a new Super Mario Bros environment.

        Args:
            rom_mode (str): the ROM mode to use when loading ROMs from disk
            stages (list): select stages at random from a specific subset

        Returns:
            None

        """
        # create a dedicated random number generator for the environment
        self.np_random = np.random.RandomState()
        # setup the environments
        self.envs = []
        # iterate over the worlds in the game, i.e., {1, ..., 8}
        for world in range(1, 9):
            # append a new list to put this world's stages into
            self.envs.append([])
            # iterate over the stages in the world, i.e., {1, ..., 4}
            for stage in range(1, 5):
                # create the target as a tuple of the world and stage
                target = (world, stage)
                # create the environment with the given ROM mode
                env = SuperMarioBrosEnv(rom_mode=rom_mode, target=target)
                # add the environment to the stage list for this world
                self.envs[-1].append(env)
        # create a placeholder for the current environment
        self.env = self.envs[0][0]
        # create a placeholder for the image viewer to render the screen
        self.viewer = None
        # create a placeholder for the subset of stages to choose
        self.stages = stages

    @property
    def screen(self):
        """Return the screen from the underlying environment"""
        return self.env.screen

    def seed(self, seed=None):
        """
        Set the seed for this environment's random number generator.

        Returns:
            list<bigint>: Returns the list of seeds used in this env's random
              number generators. The first value in the list should be the
              "main" seed, or the value which a reproducer should pass to
              'seed'. Often, the main seed equals the provided 'seed', but
              this won't be true if seed=None, for example.

        """
        # if there is no seed, return an empty list
        if seed is None:
            return []
        # set the random number seed for the NumPy random number generator
        self.np_random.seed(seed)
        # return the list of seeds used by RNG(s) in the environment
        return [seed]

    def reset(self, seed=None, options=None, return_info=None):
        """
        Reset the state of the environment and returns an initial observation.

        Args:
            seed (int): an optional random number seed for the next episode
            options (dict): An optional options for resetting the environment.
                Can include the key 'stages' to override the random set of
                stages to sample from.
            return_info (any): unused

        Returns:
            state (np.ndarray): next frame as a result of the given action

        """
        # Seed the RNG for this environment.
        self.seed(seed)
        # Get the collection of stages to sample from
        stages = self.stages
        if options is not None and 'stages' in options:
            stages = options['stages']
        # Select a random level
        if stages is not None and len(stages) > 0:
            level = self.np_random.choice(stages)
            world, stage = level.split('-')
            world = int(world) - 1
            stage = int(stage) - 1
        else:
            world = self.np_random.randint(1, 9) - 1
            stage = self.np_random.randint(1, 5) - 1
        # Set the environment based on the world and stage.
        self.env = self.envs[world][stage]
        # reset the environment
        return self.env.reset(
            seed=seed,
            options=options,
            return_info=return_info
        )

    def step(self, action):
        """
        Run one frame of the NES and return the relevant observation data.

        Args:
            action (byte): the bitmap determining which buttons to press

        Returns:
            a tuple of:
            - state (np.ndarray): next frame as a result of the given action
            - reward (float) : amount of reward returned after given action
            - done (boolean): whether the episode has ended
            - info (dict): contains auxiliary diagnostic information

        """
        return self.env.step(action)

    def close(self):
        """Close the environment."""
        # make sure the environment hasn't already been closed
        if self.env is None:
            raise ValueError('env has already been closed.')
        # iterate over each list of stages
        for stage_lists in self.envs:
            # iterate over each stage
            for stage in stage_lists:
                # close the environment
                stage.close()
        # close the environment permanently
        self.env = None
        # if there is an image viewer open, delete it
        if self.viewer is not None:
            self.viewer.close()

    def render(self, mode='human'):
        """
        Render the environment.

        Args:
            mode (str): the mode to render with:
            - human: render to the current display
            - rgb_array: Return an numpy.ndarray with shape (x, y, 3),
              representing RGB values for an x-by-y pixel image

        Returns:
            a numpy array if mode is 'rgb_array', None otherwise

        """
        return SuperMarioBrosEnv.render(self, mode=mode)

    def get_keys_to_action(self):
        """Return the dictionary of keyboard keys to actions."""
        return self.env.get_keys_to_action()

    def get_action_meanings(self):
        """Return the list of strings describing the action space actions."""
        return self.env.get_action_meanings()


# explicitly define the outward facing API of this module
__all__ = [SuperMarioBrosRandomStagesEnv.__name__]
