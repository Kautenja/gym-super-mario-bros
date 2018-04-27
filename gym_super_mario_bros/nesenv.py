"""A simple environment for interacting with the NES emulator."""
import os
import subprocess
import struct
import numpy as np
import gym
from gym.envs.classic_control.rendering import SimpleImageViewer
from .palette import PALETTE


# A separator used to split pieces of string commands sent to the emulator
SEP = '|'


# The width of images rendered by the NES
SCREEN_WIDTH = 256
# The height of images rendered by the NES
SCREEN_HEIGHT = 224


class NESEnv(gym.Env, gym.utils.EzPickle):
    """An environment for playing NES games in OpenAI Gym using FCEUX."""

    # meta-data about the environment
    metadata = {'render.modes': ['human', 'rgb_array']}

    # a pipe from the emulator (FCEUX) to client (self)
    _pipe_in_name = '/tmp/smb-pipe-in'
    # a pipe from the client (self) to emulator (FCEUX)
    _pipe_out_name = '/tmp/smb-pipe-out'

    def __init__(self,
        max_episode_steps: int,
        frame_skip: int=4,
        fceux_args: list=('--nogui', '--sound 0'),
        random_seed: int=0,
    ) -> None:
        """
        Initialize a new NES environment.

        Args:
            max_episode_steps: the math number of steps per episode.
                - pass math.inf to use no max_episode_steps limit
            frame_skip: the number of frames to skip between between inputs
            fceux_args: arguments to pass to the FCEUX command
            random_seed: the random seed to start the environment with

        Returns:
            None

        """
        gym.utils.EzPickle.__init__(self)
        self.max_episode_steps = max_episode_steps
        self.frame_skip = frame_skip
        self.fceux_args = fceux_args
        self.curr_seed = random_seed
        # setup the frame rate based on the frame skip rate
        self.metadata['video.frames_per_second'] = 60 / self.frame_skip
        self.viewer = None
        self.step_number = 0
        # these store the pipe for communicating with the environment
        self.pipe_in = None
        self.pipe_out = None
        # variables for the ROM and FCEUX interface files
        self.rom_file_path = None
        self.lua_interface_path = None
        self.emulator_started = False
        # Setup the observation space
        self.observation_space = gym.spaces.Box(
            low=0,
            high=255,
            shape=(SCREEN_HEIGHT, SCREEN_WIDTH, 3),
            dtype=np.uint8
        )
        self.screen = self.observation_space.sample()
        # Setup the action space
        self.actions = [
            'U', 'D', 'L', 'R',
            'UR', 'DR', 'URA', 'DRB',
            'A', 'B', 'RB', 'RA']
        self.action_space = gym.spaces.Discrete(len(self.actions))

    # MARK: FCEUX

    def _start_emulator(self) -> None:
        """Spawn an instance of FCEUX and pass parameters to it."""
        # validate that the rom file and lua interface are defiend
        if not self.rom_file_path:
            raise Exception('No rom file specified!')
        if not self.lua_interface_path:
            raise Exception("Must specify a lua interface file to get scores!")
        # setup the environment variables to pass to the emulator instance
        os.environ['frame_skip'] = str(self.frame_skip)
        # TODO: define and setup different reward schemes to initialize with
        # and activate them here using the environment key 'reward_scheme'

        # open up the pipes to the emulator.
        self._open_pipes()
        # build the FCEUX command
        command = ' '.join([
            'fceux',
            *self.fceux_args,
            '--loadlua',
            self.lua_interface_path,
            self.rom_file_path,
            '&'
        ])
        # open the FCEUX process
        proc = subprocess.Popen(command, shell=True)
        proc.communicate()
        # open the pipe files
        self.pipe_in = open(self._pipe_in_name, 'rb')
        self.pipe_out = open(self._pipe_out_name, 'w', 1)
        # make sure the emulator sends the ready message
        opcode, _ = self._read_from_pipe()
        assert 'ready' == opcode
        self.emulator_started = True

    def _joypad(self, button: str) -> None:
        """
        Pass a joy-pad command to the emulator

        Args:
            button: the button (or combination) to press on the controller

        Returns:
            None

        """
        self._write_to_pipe('joypad' + SEP + button)

    def _get_state(self) -> tuple:
        """
        Parse a state message from the emulator and return it.

        Returns:
            a tuple of:
            -   the screen from the emulator
            -   the reward from the previous action
            -   the terminal flag denoting if an episode has ended

        """
        # read the initial state from the pipe
        opcode, data = self._read_from_pipe()
        assert opcode == 'state'
        # The first two underscores are `reward` and `done`. the last one is
        # the dummy '\n' at the end of each line
        reward, done, screen, _ = data
        reward = int(reward.decode('ascii'))
        done = bool(int(done.decode('ascii')))
        # change the done flag to true if this step passes the episode length
        done = True if self.step_number > self.max_episode_steps else done

        # unwrap the P value representing a frame from the data
        pvs = np.array(struct.unpack('B'*len(screen), screen))
        # use the palette to convert the p values to RGB
        rgb = np.array(PALETTE[pvs-20], dtype=np.uint8)
        # reshape the screen and assign it to self
        screen = rgb.reshape((SCREEN_HEIGHT, SCREEN_WIDTH, 3))

        return screen, reward, done

    # MARK: Pipes

    def _open_pipes(self) -> None:
        """Open the communication path between self and the emulator"""
        # Open the inbound pipe if it doesn't exist yet
        if not os.path.exists(self._pipe_in_name):
            os.mkfifo(self._pipe_in_name)
        # Open the outbound pipe if it doesn't exist yet
        if not os.path.exists(self._pipe_out_name):
            os.mkfifo(self._pipe_out_name)

    def _write_to_pipe(self, message: str) -> None:
        """Write a message to the outbound pip (emulator)."""
        # write the message to the pipe and flush it
        self.pipe_out.write(message + '\n')
        self.pipe_out.flush()

    def _read_from_pipe(self) -> tuple:
        """
        Read a message from the pipe.

        Returns:
            a tuple of
            -   the opcode
            -   the data with the message (as another tuple)

        """
        # Read a message from the pipe and separate along the delimiter 0xff
        message = self.pipe_in.readline().split(b'\xFF')
        # decode the opcde
        opcode = message[0].decode('ascii')
        # return the opcode and data tuple
        return opcode, message[1:]

    # MARK: OpenAI Gym API

    def step(self, action: int) -> tuple:
        """
        Take a step using the given action.

        Args:
            action: the discrete action to perform. will use the action in
                    `self.actions` indexed by this value

        Returns:
            a tuple of:
            -   the start as a result of the action
            -   the reward achieved by taking the action
            -   a flag denoting whether the episode has ended
            -   a dictionary of additional information

        """
        # unwrap the string action value from the list of actions
        self._joypad(self.actions[action])
        # increment the frame counter
        self.step_number += 1
        # get the screen, reward, and done flag from the emulator
        self.screen, reward, done = self._get_state()

        return self.screen.copy(), reward, done, {}

    def reset(self) -> np.ndarray:
        """Reset the emulator and return the initial state."""
        if not self.emulator_started:
            self._start_emulator()
        # write the reset command to the emulator
        self._write_to_pipe('reset' + SEP)
        self.step_number = 0
        # get a state from the emulator. ignore the `reward` and `done` flag
        self.screen, _, _ = self._get_state()

        return self.screen

    def render(self, mode: str='human'):
        """
        Render the current screen using the given mode.

        Args:
            mode: the mode to render the screen using
                - 'human': render in a window using GTK
                - 'rgb_array': render in the back-end and return a matrix

        Returns:
            None if mode is 'human' or a matrix if mode is 'rgb_array'

        """
        if mode == 'human':
            if self.viewer is None:
                self.viewer = SimpleImageViewer()
            self.viewer.imshow(self.screen)
        elif mode == 'rgb_array':
            return self.screen

    def close(self) -> None:
        """Close the emulator and shutdown FCEUX."""
        self._write_to_pipe('close')
        self.pipe_in.close()
        self.pipe_out.close()
        self.emulator_started = False

    def seed(self, seed: int=None) -> list:
        """
        Set the seed for this env's random number generator(s).

        Returns:
            A list of seeds used in this env's random number generators.
            there is only one "main" seed in this env
        """
        self.curr_seed = gym.utils.seeding.hash_seed(seed) % 256
        return [self.curr_seed]


__all__ = [NESEnv.__name__]
