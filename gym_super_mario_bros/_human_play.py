"""A method to play gym environments using human IO inputs."""
import os
import gym
import pygame
from typing import Callable


def display_arr(screen, arr, video_size, transpose):
    arr_min, arr_max = arr.min(), arr.max()
    arr = 255.0 * (arr - arr_min) / (arr_max - arr_min)
    pyg_img = pygame.surfarray.make_surface(arr.swapaxes(0, 1) if transpose else arr)
    pyg_img = pygame.transform.scale(pyg_img, video_size)
    screen.blit(pyg_img, (0,0))


def play(env: gym.Env,
    transpose: bool=True,
    fps: int=30,
    callback: Callable=None,
    nop_: any=0,
) -> None:
    """Play the game using the keyboard as a human.

    Args:
        env: gym.Env
            Environment to use for playing.
        transpose: bool
            If True the output of observation is transposed.
            Defaults to true.
        fps: int
            Maximum number of steps of the environment to execute every second.
            Defaults to 30.
        callback: lambda or None
            Callback if a callback is provided it will be executed after
            every step. It takes the following input:
                obs_t: observation before performing action
                obs_tp1: observation after performing action
                action: action that was executed
                rew: reward that was received
                done: whether the environemnt is done or not
                info: debug info
        nop_: the object to use as a null op action for the environment

    Returns:
        None

    """
    # type check the observation space
    obs_s = env.observation_space
    assert type(obs_s) == gym.spaces.box.Box
    assert len(obs_s.shape) == 2 or (len(obs_s.shape) == 3 and obs_s.shape[2] in [1,3])
    # get the mapping of keyboard keys to actions in the environment
    if hasattr(env, 'get_keys_to_action'):
        keys_to_action = env.get_keys_to_action()
    elif hasattr(env.unwrapped, 'get_keys_to_action'):
        keys_to_action = env.unwrapped.get_keys_to_action()
    else:
        raise ValueError('env has no get_keys_to_action method')
    relevant_keys = set(sum(map(list, keys_to_action.keys()),[]))
    # transpose the video is specified
    if transpose:
        video_size = env.observation_space.shape[1], env.observation_space.shape[0]
    else:
        video_size = env.observation_space.shape[0], env.observation_space.shape[1]

    pressed_keys = []
    running = True
    env_done = True
    # setup the screen using pygame
    screen = pygame.display.set_mode(video_size)
    pygame.display.set_caption(env.spec.id)
    # disable the SDL video driver so FCEUX wont open a window
    os.environ['SDL_VIDEODRIVER'] = 'dummy'
    clock = pygame.time.Clock()
    # start the main game loop
    while running:
        if env_done:
            env_done = False
            obs = env.reset()
        else:
            action = keys_to_action.get(tuple(sorted(pressed_keys)), nop_)
            prev_obs = obs
            obs, rew, env_done, info = env.step(action)
            if callback is not None:
                callback(prev_obs, obs, action, rew, env_done, info)
        if obs is not None:
            if len(obs.shape) == 2:
                obs = obs[:, :, None]
            if obs.shape[2] == 1:
                obs = obs.repeat(3, axis=2)
            display_arr(screen, obs, transpose=transpose, video_size=video_size)

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
