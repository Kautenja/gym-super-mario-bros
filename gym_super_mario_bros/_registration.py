"""Registration code of Gym environments in this package."""
import gym
from ._rom_mode import RomMode


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
_register_mario_env('SuperMarioBros-v0', frameskip=4, rom_mode=RomMode.VANILLA)
_register_mario_env('SuperMarioBros-v1', frameskip=4, rom_mode=RomMode.DOWNSAMPLE)
_register_mario_env('SuperMarioBros-v2', frameskip=4, rom_mode=RomMode.PIXEL)
_register_mario_env('SuperMarioBros-v3', frameskip=4, rom_mode=RomMode.RECTANGLE)


# Super Mario Bros. with no frame skip
_register_mario_env('SuperMarioBrosNoFrameskip-v0', frameskip=1, rom_mode=RomMode.VANILLA)
_register_mario_env('SuperMarioBrosNoFrameskip-v1', frameskip=1, rom_mode=RomMode.DOWNSAMPLE)
_register_mario_env('SuperMarioBrosNoFrameskip-v2', frameskip=1, rom_mode=RomMode.PIXEL)
_register_mario_env('SuperMarioBrosNoFrameskip-v3', frameskip=1, rom_mode=RomMode.RECTANGLE)


# Super Mario Bros. 2 (Lost Levels) with standard frame skip
_register_mario_env('SuperMarioBros2-v0', lost_levels=True, frameskip=4, rom_mode=RomMode.VANILLA)
_register_mario_env('SuperMarioBros2-v1', lost_levels=True, frameskip=4, rom_mode=RomMode.DOWNSAMPLE)


# Super Mario Bros. 2 (Lost Levels) with no frame skip
_register_mario_env('SuperMarioBros2NoFrameskip-v0', lost_levels=True, frameskip=1, rom_mode=RomMode.VANILLA)
_register_mario_env('SuperMarioBros2NoFrameskip-v1', lost_levels=True, frameskip=1, rom_mode=RomMode.DOWNSAMPLE)


def _register_mario_level_env(id, **kwargs):
    """
    Register a Super Mario Bros. (1/2) Level environment with OpenAI Gym.

    Args:
        id (str): id for the env to register
        kwargs (dict): keyword arguments for the SuperMarioBrosLevelEnv initializer

    Returns:
        None

    """
    kwargs['max_episode_steps'] = float('inf')
    # register the environment
    gym.envs.registration.register(
        id=id,
        entry_point='gym_super_mario_bros:SuperMarioBrosLevelEnv',
        max_episode_steps=9999999,
        reward_threshold=32000,
        kwargs=kwargs,
        nondeterministic=True,
    )


# a template for making individual level environments
_ID_TEMPLATE = 'SuperMarioBros{}-{}-{}-v{}'
# iterate over all the rom modes, worlds (1-8), and levels (1-4)
_ROM_MODES = [
    RomMode.VANILLA,
    RomMode.DOWNSAMPLE,
    RomMode.PIXEL,
    RomMode.RECTANGLE
]
for version, rom_mode in enumerate(_ROM_MODES):
    for world in range(1, 9):
        for level in range(1, 5):
            # setup the frame-skipping environment
            env_id = _ID_TEMPLATE.format('', world, level, version)
            _register_mario_level_env(env_id,
                frameskip=4,
                rom_mode=rom_mode,
                target_world=world,
                target_level=level
            )
            # setup the no frame-skipping environment
            env_id = _ID_TEMPLATE.format('NoFrameskip', world, level, version)
            _register_mario_level_env(env_id,
                frameskip=1,
                rom_mode=rom_mode,
                target_world=world,
                target_level=level
            )


# create an alias to gym.make for ease of access
make = gym.make


# define the outward facing API of this module (none, gym provides the API)
__all__ = [make.__name__]
