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


def _register_mario_env(id, **kwargs):
    """
    Register a Super Mario Bros. (1/2) environment with Gymnasium.

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


def _register_smb2_usa_env(id, **kwargs):
    """
    Register a Super Mario Bros. 2 (USA) environment with Gymnasium.

    Args:
        id (str): id for the env to register
        kwargs (dict): keyword arguments for the SuperMarioBros2Env initializer

    Returns:
        None

    """
    gym.envs.registration.register(
        id=id,
        entry_point='gym_super_mario_bros:SuperMarioBros2Env',
        max_episode_steps=_MAX_EPISODE_STEPS,
        reward_threshold=_REWARD_THRESHOLD,
        kwargs=kwargs,
        nondeterministic=True,
        disable_env_checker=_DISABLE_ENV_CHECKER,
    )


def _register_smb3_env(id, **kwargs):
    """
    Register a Super Mario Bros. 3 environment with Gymnasium.

    Args:
        id (str): id for the env to register
        kwargs (dict): keyword arguments for the SuperMarioBros3Env initializer

    Returns:
        None

    """
    gym.envs.registration.register(
        id=id,
        entry_point='gym_super_mario_bros:SuperMarioBros3Env',
        max_episode_steps=_MAX_EPISODE_STEPS,
        reward_threshold=_REWARD_THRESHOLD,
        kwargs=kwargs,
        nondeterministic=True,
        disable_env_checker=_DISABLE_ENV_CHECKER,
    )


# Super Mario Bros.
_register_mario_env('SuperMarioBros-v0')


# Super Mario Bros. 2 (Lost Levels)
_register_mario_env('SuperMarioBros2-v0', lost_levels=True)


# Super Mario Bros. 2 (USA)
_register_smb2_usa_env('SuperMarioBros2USA-v0')


# Super Mario Bros. 3
_register_smb3_env('SuperMarioBros3-v0')


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
_SMB2_USA_STAGES_PER_WORLD = (3, 3, 3, 3, 3, 3, 2)


def _lost_levels_world_label(world):
    """Return the public world label for a Lost Levels world number."""
    if world <= 9:
        return str(world)
    return chr(ord('A') + world - 10)


# iterate over Super Mario Bros. worlds (1-8) and stages (1-4)
for world in range(1, 9):
    for stage in range(1, 5):
        target = (world, stage)
        env_id = _ID_TEMPLATE.format('', world, stage, 0)
        _register_mario_stage_env(env_id, target=target)
        env_id = _ID_ALIAS_TEMPLATE.format(world, stage, 0)
        _register_mario_stage_env(env_id, target=target)


# iterate over Lost Levels worlds (1-9, A-D) and stages (1-4)
for world in range(1, 14):
    for stage in range(1, 5):
        target = (world, stage)
        env_id = _ID_TEMPLATE.format(
            '2',
            _lost_levels_world_label(world),
            stage,
            0,
        )
        _register_mario_stage_env(
            env_id,
            lost_levels=True,
            target=target,
        )


# iterate over Super Mario Bros. 2 (USA) worlds (1-7) and stages
for world, stage_count in enumerate(_SMB2_USA_STAGES_PER_WORLD, start=1):
    for stage in range(1, stage_count + 1):
        env_id = 'SuperMarioBros2USA-{}-{}-v0'.format(world, stage)
        _register_smb2_usa_env(env_id, target=(world, stage))


# Super Mario Bros. 3 has a validated vanilla World 1-1 entry point.
_register_smb3_env('SuperMarioBros3-1-1-v0', target=(1, 1))


# create an alias to gymnasium.make for ease of access
make = gym.make


# define the outward facing API of this module (none, gymnasium provides the API)
__all__ = ['make']
