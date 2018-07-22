"""A method to play gym environments using human IO inputs."""
import os
import gym
import pygame
import numpy as np
from .visualize.realtime_plot import RealtimePlot


def display_arr(screen, arr, video_size, transpose):
    """
    Display an image to the pygame screen.

    Args:
        screen (pygame.Surface): the pygame surface to write frames to
        arr (np.ndarray): numpy array representing a single frame of gameplay
        video_size (tuple): the size to render the frame as
        transpose (bool): whether to transpose the frame before displaying

    Returns:
        None

    """
    # take the transpose if necessary
    if transpose:
        pyg_img = pygame.surfarray.make_surface(arr.swapaxes(0, 1))
    else:
        pyg_img = arr
    # resize the image according to given image size
    pyg_img = pygame.transform.scale(pyg_img, video_size)
    # blit the image to the surface
    screen.blit(pyg_img, (0, 0))


def play(env, transpose=True, fps=30, callback=None, nop_=0):
    """Play the game using the keyboard as a human.

    Args:
        env (gym.Env): the environment to use for playing
        transpose (bool): whether to transpose frame before viewing them
        fps (int): number of steps of the environment to execute every second
        callback (Callable): a callback to execute after every step.
            It takes the following inputs:
            - state: observation before performing action
            - next_state: observation after performing action
            - action: action that fired
            - reward: reward from the action taken
            - done: a flag to determine if the episode is over
            - info: extra information from the environment
        nop_ (any): the object to use as a null op action for the environment

    Returns:
        None

    """
    # ensure the observation space is a box of pixels
    assert isinstance(env.observation_space, gym.spaces.box.Box)
    # ensure the observation space is either B&W pixels or RGB Pixels
    obs_s = env.observation_space
    is_bw = len(obs_s.shape) == 2
    is_rgb = len(obs_s.shape) == 3 and obs_s.shape[2] in [1, 3]
    assert is_bw or is_rgb
    # get the mapping of keyboard keys to actions in the environment
    if hasattr(env, 'get_keys_to_action'):
        keys_to_action = env.get_keys_to_action()
    elif hasattr(env.unwrapped, 'get_keys_to_action'):
        keys_to_action = env.unwrapped.get_keys_to_action()
    else:
        raise ValueError('env has no get_keys_to_action method')
    relevant_keys = set(sum(map(list, keys_to_action.keys()), []))
    # determine the size of the video in pixels
    video_size = env.observation_space.shape[0], env.observation_space.shape[1]
    if transpose:
        video_size = tuple(reversed(video_size))
    # generate variables to determine the running state of the game
    pressed_keys = []
    running = True
    env_done = True
    # setup the screen using pygame
    screen = pygame.display.set_mode(video_size)
    pygame.display.set_caption(env.spec.id)
    # disable the SDL video driver so FCEUX wont open a window
    os.environ['SDL_VIDEODRIVER'] = 'dummy'
    clock = pygame.time.Clock()
    plot = RealtimePlot()
    # start the main game loop
    while running:
        if env_done:
            env_done = False
            obs = env.reset()
        else:
            action = keys_to_action.get(tuple(sorted(pressed_keys)), nop_)
            prev_obs = obs
            obs, rew, env_done, info = env.step(action)
            plot(rew)
            if callback is not None:
                callback(prev_obs, obs, action, rew, env_done, info)
        if obs is not None:
            if len(obs.shape) == 2:
                obs = obs[:, :, None]
            if obs.shape[2] == 1:
                obs = obs.repeat(3, axis=2)
            display_arr(screen, obs, video_size, transpose)

        # process pygame events
        for event in pygame.event.get():
            # test events, set key states
            if event.type == pygame.KEYDOWN:
                if event.key in relevant_keys:
                    pressed_keys.append(event.key)
                elif event.key == 27:
                    running = False
            elif event.type == pygame.KEYUP:
                if event.key in relevant_keys:
                    pressed_keys.remove(event.key)
            elif event.type == pygame.QUIT:
                running = False

        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()


# explicitly define the outward facing API of the module
__all__ = [play.__name__]
