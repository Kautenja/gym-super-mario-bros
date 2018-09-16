"""Registration code of Gym environments in this package."""
import gym


def _register_mario_env(id, **kwargs):
    """
    Register a Super Mario Bros. (1/2) environment with OpenAI Gym.

    Args:
        id (str): id for the env to register
        kwargs (dict): keyword arguments for the SuperMarioBrosEnv initializer

    Returns:
        None

    """
    kwargs['max_episode_steps'] = float('inf')
    # register the environment
    gym.envs.registration.register(
        id=id,
        entry_point='gym_super_mario_bros:SuperMarioBrosEnv',
        max_episode_steps=9999999,
        reward_threshold=32000,
        kwargs=kwargs,
        nondeterministic=True,
    )


# Super Mario Bros. with standard frame skip
_register_mario_env('SuperMarioBros-v0', frames_per_step=4, rom_mode='vanilla')
_register_mario_env('SuperMarioBros-v1', frames_per_step=4, rom_mode='downsample')
_register_mario_env('SuperMarioBros-v2', frames_per_step=4, rom_mode='pixel')
_register_mario_env('SuperMarioBros-v3', frames_per_step=4, rom_mode='rectangle')


# Super Mario Bros. with no frame skip
_register_mario_env('SuperMarioBrosNoFrameskip-v0', frames_per_step=1, rom_mode='vanilla')
_register_mario_env('SuperMarioBrosNoFrameskip-v1', frames_per_step=1, rom_mode='downsample')
_register_mario_env('SuperMarioBrosNoFrameskip-v2', frames_per_step=1, rom_mode='pixel')
_register_mario_env('SuperMarioBrosNoFrameskip-v3', frames_per_step=1, rom_mode='rectangle')


# Super Mario Bros. 2 (Lost Levels) with standard frame skip
_register_mario_env('SuperMarioBros2-v0', lost_levels=True, frames_per_step=4, rom_mode='vanilla')
_register_mario_env('SuperMarioBros2-v1', lost_levels=True, frames_per_step=4, rom_mode='downsample')


# Super Mario Bros. 2 (Lost Levels) with no frame skip
_register_mario_env('SuperMarioBros2NoFrameskip-v0', lost_levels=True, frames_per_step=1, rom_mode='vanilla')
_register_mario_env('SuperMarioBros2NoFrameskip-v1', lost_levels=True, frames_per_step=1, rom_mode='downsample')


def _register_mario_stage_env(id, **kwargs):
    """
    Register a Super Mario Bros. (1/2) stage environment with OpenAI Gym.

    Args:
        id (str): id for the env to register
        kwargs (dict): keyword arguments for the SuperMarioBrosEnv initializer

    Returns:
        None

    """
    kwargs['max_episode_steps'] = float('inf')
    # register the environment
    gym.envs.registration.register(
        id=id,
        entry_point='gym_super_mario_bros:SuperMarioBrosEnv',
        max_episode_steps=9999999,
        reward_threshold=32000,
        kwargs=kwargs,
        nondeterministic=True,
    )


# a template for making individual stage environments
_ID_TEMPLATE = 'SuperMarioBros{}-{}-{}-v{}'
# iterate over all the rom modes, worlds (1-8), and stages (1-4)
_ROM_MODES = [
    'vanilla',
    'downsample',
    'pixel',
    'rectangle'
]
for version, rom_mode in enumerate(_ROM_MODES):
    for world in range(1, 9):
        for stage in range(1, 5):
            # setup the frame-skipping environment
            env_id = _ID_TEMPLATE.format('', world, stage, version)
            _register_mario_stage_env(env_id,
                frames_per_step=4,
                rom_mode=rom_mode,
                target=(world, stage),
            )
            # setup the no frame-skipping environment
            env_id = _ID_TEMPLATE.format('NoFrameskip', world, stage, version)
            _register_mario_stage_env(env_id,
                frames_per_step=1,
                rom_mode=rom_mode,
                target=(world, stage),
            )


# create an alias to gym.make for ease of access
make = gym.make


# define the outward facing API of this module (none, gym provides the API)
__all__ = [make.__name__]
