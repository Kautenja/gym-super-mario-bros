"""Registration code of Gymnasium environments in this package."""
import gymnasium as gym


_MAX_EPISODE_STEPS = 9999999
_REWARD_THRESHOLD = 9999999
_DISABLE_ENV_CHECKER = True
# Gymnasium's passive checker is intentionally disabled for registered NES
# environments because construction eagerly loads ROM-backed emulator state and
# skips intro frames. The test suite covers reset/step/render compatibility
# directly without running the checker for every registered variant.
_DISABLE_ENV_CHECKER_REASON = (
    'ROM-backed NES environment compatibility is covered by package smoke '
    'tests instead of Gymnasium passive checker construction probes.'
)


def _register_mario_env(id, is_random=False, **kwargs):
    """
    Register a Super Mario Bros. (1/2) environment with Gymnasium.

    Args:
        id (str): id for the env to register
        is_random (bool): whether to use the random levels environment
        kwargs (dict): keyword arguments for the SuperMarioBrosEnv initializer

    Returns:
        None

    """
    # if the is random flag is set
    if is_random:
        # set the entry point to the random level environment
        entry_point = 'gym_super_mario_bros:SuperMarioBrosRandomStagesEnv'
    else:
        # set the entry point to the standard Super Mario Bros. environment
        entry_point = 'gym_super_mario_bros:SuperMarioBrosEnv'
    # register the environment
    gym.envs.registration.register(
        id=id,
        entry_point=entry_point,
        # Preserve Gymnasium TimeLimit wrapping while keeping the historical
        # registration cap effectively unreachable during normal game play.
        max_episode_steps=_MAX_EPISODE_STEPS,
        reward_threshold=_REWARD_THRESHOLD,
        kwargs=kwargs,
        nondeterministic=True,
        disable_env_checker=_DISABLE_ENV_CHECKER,
    )


# Super Mario Bros.
_register_mario_env('SuperMarioBros-v0', rom_mode='vanilla')
_register_mario_env('SuperMarioBros-v1', rom_mode='downsample')
_register_mario_env('SuperMarioBros-v2', rom_mode='pixel')
_register_mario_env('SuperMarioBros-v3', rom_mode='rectangle')


# Super Mario Bros. Random Levels
_register_mario_env('SuperMarioBrosRandomStages-v0', is_random=True, rom_mode='vanilla')
_register_mario_env('SuperMarioBrosRandomStages-v1', is_random=True, rom_mode='downsample')
_register_mario_env('SuperMarioBrosRandomStages-v2', is_random=True, rom_mode='pixel')
_register_mario_env('SuperMarioBrosRandomStages-v3', is_random=True, rom_mode='rectangle')


# Super Mario Bros. 2 (Lost Levels)
_register_mario_env('SuperMarioBros2-v0', lost_levels=True, rom_mode='vanilla')
_register_mario_env('SuperMarioBros2-v1', lost_levels=True, rom_mode='downsample')


def _register_mario_stage_env(id, **kwargs):
    """
    Register a Super Mario Bros. (1/2) stage environment with Gymnasium.

    Args:
        id (str): id for the env to register
        kwargs (dict): keyword arguments for the SuperMarioBrosEnv initializer

    Returns:
        None

    """
    # register the environment
    gym.envs.registration.register(
        id=id,
        entry_point='gym_super_mario_bros:SuperMarioBrosEnv',
        # Preserve Gymnasium TimeLimit wrapping while keeping the historical
        # registration cap effectively unreachable during normal game play.
        max_episode_steps=_MAX_EPISODE_STEPS,
        reward_threshold=_REWARD_THRESHOLD,
        kwargs=kwargs,
        nondeterministic=True,
        disable_env_checker=_DISABLE_ENV_CHECKER,
    )


# a template for making individual stage environments
_ID_TEMPLATE = 'SuperMarioBros{}-{}-{}-v{}'
# Gymnasium smoke tests and downstream callers may omit the separator between
# the game name and world number; keep the historical IDs and add aliases.
_ID_ALIAS_TEMPLATE = 'SuperMarioBros{}-{}-v{}'
# A list of ROM modes for each level environment
_ROM_MODES = [
    'vanilla',
    'downsample',
    'pixel',
    'rectangle'
]


# iterate over all the rom modes, worlds (1-8), and stages (1-4)
for version, rom_mode in enumerate(_ROM_MODES):
    for world in range(1, 9):
        for stage in range(1, 5):
            # create the target
            target = (world, stage)
            # setup the frame-skipping environment
            env_id = _ID_TEMPLATE.format('', world, stage, version)
            _register_mario_stage_env(env_id, rom_mode=rom_mode, target=target)
            env_id = _ID_ALIAS_TEMPLATE.format(world, stage, version)
            _register_mario_stage_env(env_id, rom_mode=rom_mode, target=target)


# create an alias to gymnasium.make for ease of access
make = gym.make


# define the outward facing API of this module (none, gymnasium provides the API)
__all__ = ['make']
