"""A simple environment for interacting with the NES emulator."""
import os
import subprocess
import struct
from threading import Thread, Condition
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
    _pipe_in_name = '/tmp/nesgym-pipe-in'
    # a pipe from the client (self) to emulator (FCEUX)
    _pipe_out_name = '/tmp/nesgym-pipe-out'

    def __init__(self,
        max_episode_steps: int,
        frame_skip: int=4,
        fceux_args: list=('--nogui', '--sound 0'),
    ) -> None:
        """
        Initialize a new NES environment.

        Args:
            max_episode_steps: the math number of steps per episode.
                - pass math.inf to use no max_episode_steps limit
            frame_skip: the number of frames to skip between between inputs
            fceux_args: arguments to pass to the FCEUX command

        Returns:
            None

        """
        gym.utils.EzPickle.__init__(self)
        self.curr_seed = 0
        self.screen = np.zeros((SCREEN_HEIGHT, SCREEN_WIDTH, 3), dtype=np.uint8)
        self.closed = False
        self.can_send_command = True
        self.command_cond = Condition()
        self.viewer = None
        self.reward = 0
        self.done = False
        self.episode_length = max_episode_steps
        self.frame_skip = frame_skip
        self.fceux_args = fceux_args

        self.actions = [
            'U', 'D', 'L', 'R',
            'UR', 'DR', 'URA', 'DRB',
            'A', 'B', 'RB', 'RA']
        self.action_space = gym.spaces.Discrete(len(self.actions))
        self.frame = 0

        self.metadata['video.frames_per_second'] = 60 / self.frame_skip

        # for communication with emulator
        self.pipe_in = None
        self.pipe_out = None

        self.rom_file_path = None
        self.lua_interface_path = None
        self.emulator_started = False

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
        self.frame += 1

        return (*self._get_state(), {})

    def reset(self) -> np.ndarray:
        """Reset the emulator and return the initial state."""
        if not self.emulator_started:
            self._start_emulator()
        # write the reset command to the emulator
        self._write_to_pipe('reset' + SEP)
        self.frame = 0
        # get a state from the emulator. ignore the `reward` and `done` flag
        screen, _, _ = self._get_state()

        return screen

    def render(self, mode='human', **kwargs):
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

    def seed(self, seed=None):
        """
        """
        self.curr_seed = gym.utils.seeding.hash_seed(seed) % 256
        return [self.curr_seed]

    def close(self):
        """Close the emulator and shutdown FCEUX."""
        self.closed = True

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
        # TODO: no matter whether it starts, proc.returncode is always zero
        self.emulator_started = True
        # open the pipe files
        self.pipe_in = open(self._pipe_in_name, 'rb')
        self.pipe_out = open(self._pipe_out_name, 'w', 1)
        # make sure the emulator sends the ready message
        opcode, _ = self._read_from_pipe()
        assert 'ready' == opcode

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
        """Parse a state message from the emulator and return it."""
        # read the initial state from the pipe
        opcode, data = self._read_from_pipe()
        assert opcode == 'state'
        # The first two underscores are `reward` and `done`. the last one is
        # the dummy '\n' at the end of each line
        reward, done, screen, _ = data
        reward = int(reward.decode('ascii'))
        done = bool(int(done.decode('ascii')))
        # change the done flag to true if this step passes the episode length
        done = True if self.frame > self.episode_length else done

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
        message = self.pipe_in.readline().split(b'\xFF')
        opcode = message[0].decode('ascii')
        return opcode, message[1:]

    # def _pipe_handler(self) -> None:
    #     """Handle messages from the emulator until the pipe is closed."""
    #     # open the inbound pipe to read bytes
    #     with open(self._pipe_in_name, 'rb') as pipe:
    #         # Loop until the connection is closed
    #         while not self.closed:
    #             # read a message from the pipe (values are delimitted by 0xff)
    #             message = pipe.readline().split(b'\xFF')
    #             opcode = message[0].decode('ascii')
    #             # print(opcode)

    #             if opcode == 'wait_for_command':
    #                 with self.command_cond:
    #                     self.can_send_command = True
    #                     self.command_cond.notifyAll()
    #             elif opcode == 'state':
    #                 self.reward = int(message[1].decode('ascii'))
    #                 self.done = bool(int(message[2].decode('ascii')))
    #                 # unwrap the P value representing a frame from the message
    #                 pvs = np.array(struct.unpack('B'*len(message[3]), message[3]))
    #                 # use the palette to convert the p values to RGB
    #                 rgb = np.array(PALETTE[pvs-20], dtype=np.uint8)
    #                 # reshape the screen and assign it to self
    #                 self.screen = rgb.reshape((SCREEN_HEIGHT, SCREEN_WIDTH, 3))


__all__ = [NESEnv.__name__]






# """A simple environment for interacting with the NES emulator."""
# import os
# import subprocess
# import struct
# from threading import Thread, Condition
# import numpy as np
# import gym
# from gym.envs.classic_control.rendering import SimpleImageViewer
# from .palette import PALETTE


# # A separator used to split pieces of string commands sent to the emulator
# SEP = '|'


# # The width of images rendered by the NES
# SCREEN_WIDTH = 256
# # The height of images rendered by the NES
# SCREEN_HEIGHT = 224


# class NESEnv(gym.Env, gym.utils.EzPickle):
#     """An environment for playing NES games in OpenAI Gym using FCEUX."""

#     # meta-data about the environment
#     metadata = {'render.modes': ['human', 'rgb_array']}

#     # a pipe from the emulator (FCEUX) to client (self)
#     _pipe_in_name = '/tmp/nesgym-pipe-in'
#     # a pipe from the client (self) to emulator (FCEUX)
#     _pipe_out_name = '/tmp/nesgym-pipe-out'

#     def __init__(self,
#         max_episode_steps: int,
#         frame_skip: int=4,
#         fceux_args: list=[
#             '--nogui',
#             '--sound 0',
#         ],
#     ) -> None:
#         """
#         Initialize a new NES environment.

#         Args:
#             max_episode_steps: the math number of steps per episode.
#                 - pass math.inf to use no max_episode_steps limit
#             frame_skip: the number of frames to skip between between inputs
#             fceux_args: arguments to pass to the FCEUX command

#         Returns:
#             None

#         """
#         gym.utils.EzPickle.__init__(self)
#         self.curr_seed = 0
#         self.screen = np.zeros((SCREEN_HEIGHT, SCREEN_WIDTH, 3), dtype=np.uint8)
#         self.closed = False
#         self.can_send_command = True
#         self.command_cond = Condition()
#         self.viewer = None
#         self.reward = 0
#         self.done = False
#         self.episode_length = max_episode_steps
#         self.frame_skip = frame_skip
#         self.fceux_args = fceux_args

#         self.actions = [
#             'U', 'D', 'L', 'R',
#             'UR', 'DR', 'URA', 'DRB',
#             'A', 'B', 'RB', 'RA']
#         self.action_space = gym.spaces.Discrete(len(self.actions))
#         self.frame = 0

#         self.metadata['video.frames_per_second'] = 60 / self.frame_skip

#         # for communication with emulator
#         self.pipe_in = None
#         self.pipe_out = None
#         self.thread_incoming = None

#         self.rom_file_path = None
#         self.lua_interface_path = None
#         self.emulator_started = False

#     # MARK: OpenAI Gym API

#     def step(self, action):
#         """
#         """
#         self.frame += 1
#         if self.done or self.frame > self.episode_length:
#             self.done = False
#             self.frame = 0
#             return self.screen.copy(), self.reward, True, {'frame': 0}
#         obs = self.screen.copy()
#         info = {"frame": self.frame}
#         with self.command_cond:
#             while not self.can_send_command:
#                 self.command_cond.wait()
#             self.can_send_command = False
#         self._joypad(self.actions[action])
#         return self.screen.copy(), self.reward, False, info

#     def reset(self):
#         """
#         """
#         if not self.emulator_started:
#             self._start_emulator()
#         self.reward = 0
#         self.screen = np.zeros((SCREEN_HEIGHT, SCREEN_WIDTH, 3), dtype=np.uint8)
#         self._write_to_pipe('reset' + SEP)
#         with self.command_cond:
#             self.can_send_command = False

#         # hacky fix: the first 3 screens of every episode were noise for some
#         # reason, so here skip the first three frames of every episode with
#         # NOPS and dont tell the agent
#         # for _ in range(3):
#         #     self.step(0)

#         return self.screen

#     def render(self, mode='human', **kwargs):
#         """
#         Render the current screen using the given mode.

#         Args:
#             mode: the mode to render the screen using
#                 - 'human': render in a window using GTK
#                 - 'rgb_array': render in the back-end and return a matrix

#         Returns:
#             None if mode is 'human' or a matrix if mode is 'rgb_array'

#         """
#         if mode == 'human':
#             if self.viewer is None:
#                 self.viewer = SimpleImageViewer()
#             self.viewer.imshow(self.screen)
#         elif mode == 'rgb_array':
#             return self.screen

#     def seed(self, seed=None):
#         """
#         """
#         self.curr_seed = gym.utils.seeding.hash_seed(seed) % 256
#         return [self.curr_seed]

#     def close(self):
#         """Close the emulator and shutdown FCEUX."""
#         self.closed = True

#     # MARK: FCEUX

#     def _start_emulator(self) -> None:
#         """Spawn an instance of FCEUX and pass parameters to it."""
#         # validate that the rom file and lua interface are defiend
#         if not self.rom_file_path:
#             raise Exception('No rom file specified!')
#         if not self.lua_interface_path:
#             raise Exception("Must specify a lua interface file to get scores!")
#         # setup the environment variables to pass to the emulator instance
#         os.environ['frame_skip'] = str(self.frame_skip)
#         # TODO: define and setup different reward schemes to initialize with
#         # and activate them here using the environment key 'reward_scheme'

#         # open up the pipes to the emulator.
#         self._open_pipes()
#         # build the FCEUX command
#         command = ' '.join([
#             'fceux',
#             *self.fceux_args,
#             '--loadlua',
#             self.lua_interface_path,
#             self.rom_file_path,
#             '&'
#         ])
#         # open the FCEUX process
#         proc = subprocess.Popen(command, shell=True)
#         proc.communicate()
#         # TODO: no matter whether it starts, proc.returncode is always zero
#         self.emulator_started = True

#     def _joypad(self, button):
#         """
#         """
#         self._write_to_pipe('joypad' + SEP + button)

#     # MARK: Pipes

#     def _open_pipes(self) -> None:
#         """Open the communication path between self and the emulator"""
#         # Open the inbound pipe if it doesn't exist yet
#         if not os.path.exists(self._pipe_in_name):
#             os.mkfifo(self._pipe_in_name)
#         # Open the outbound pipe if it doesn't exist yet
#         if not os.path.exists(self._pipe_out_name):
#             os.mkfifo(self._pipe_out_name)
#         # Setup the thread for listening for messages from the emulator
#         self.thread_incoming = Thread(target=self._pipe_handler)
#         self.thread_incoming.start()

#     def _write_to_pipe(self, message: str) -> None:
#         """Write a message to the outbound pip (emulator)."""
#         if not self.pipe_out:
#             # arg 1 for line buffering - see python doc
#             self.pipe_out = open(self._pipe_out_name, 'w', 1)
#         self.pipe_out.write(message + '\n')
#         self.pipe_out.flush()

#     def _pipe_handler(self) -> None:
#         """Handle messages from the emulator until the pipe is closed."""
#         # open the inbound pipe to read bytes
#         with open(self._pipe_in_name, 'rb') as pipe:
#             # Loop until the connection is closed
#             while not self.closed:
#                 # read a message from the pipe (values are delimitted by 0xff)
#                 message = pipe.readline().split(b'\xFF')
#                 opcode = message[0].decode('ascii')
#                 # print(opcode)

#                 if opcode == 'wait_for_command':
#                     with self.command_cond:
#                         self.can_send_command = True
#                         self.command_cond.notifyAll()
#                 elif opcode == 'state':
#                     self.reward = int(message[1].decode('ascii'))
#                     self.done = bool(int(message[2].decode('ascii')))
#                     # unwrap the P value representing a frame from the message
#                     pvs = np.array(struct.unpack('B'*len(message[3]), message[3]))
#                     # use the palette to convert the p values to RGB
#                     rgb = np.array(PALETTE[pvs-20], dtype=np.uint8)
#                     # reshape the screen and assign it to self
#                     self.screen = rgb.reshape((SCREEN_HEIGHT, SCREEN_WIDTH, 3))


# __all__ = [NESEnv.__name__]
