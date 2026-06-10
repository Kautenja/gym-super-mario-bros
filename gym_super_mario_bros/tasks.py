"""Task metadata for registered Super Mario Bros. environments."""
from dataclasses import dataclass


SMB1_ROM_MODES = ('vanilla',)
LOST_LEVELS_ROM_MODES = ('vanilla',)
SMB2_USA_STAGES_PER_WORLD = (3, 3, 3, 3, 3, 3, 2)
SMB3_VALIDATED_STAGES = ((1, 1),)


@dataclass(frozen=True)
class MarioTask:
    """A queryable description of one registered Mario task."""

    env_id: str
    game: str
    game_family: str
    version: int
    rom_mode: str
    world: int | None = None
    stage: int | None = None
    world_label: str | None = None
    single_stage: bool = False
    alias_of: str | None = None
    train_split: bool = True
    eval_split: bool = True
    validated: bool = True

    @property
    def task_id(self):
        """Return the stable task identifier for conditioning/evaluation."""
        return self.alias_of or self.env_id

    def to_dict(self):
        """Return this task as a plain dictionary."""
        return dict(
            env_id=self.env_id,
            task_id=self.task_id,
            game=self.game,
            game_family=self.game_family,
            version=self.version,
            rom_mode=self.rom_mode,
            world=self.world,
            stage=self.stage,
            world_label=self.world_label,
            single_stage=self.single_stage,
            alias_of=self.alias_of,
            train_split=self.train_split,
            eval_split=self.eval_split,
            validated=self.validated,
        )


def _lost_levels_world_label(world):
    """Return the public world label for a Lost Levels world number."""
    if world <= 9:
        return str(world)
    return chr(ord('A') + world - 10)


def _build_tasks():
    """Build the package task inventory from the registered env surface."""
    tasks = []

    for version, rom_mode in enumerate(SMB1_ROM_MODES):
        tasks.append(MarioTask(
            env_id='SuperMarioBros-v{}'.format(version),
            game='smb1',
            game_family='smb1',
            version=version,
            rom_mode=rom_mode,
        ))

        for world in range(1, 9):
            for stage in range(1, 5):
                canonical_env_id = 'SuperMarioBros-{}-{}-v{}'.format(
                    world,
                    stage,
                    version,
                )
                tasks.append(MarioTask(
                    env_id=canonical_env_id,
                    game='smb1',
                    game_family='smb1',
                    version=version,
                    rom_mode=rom_mode,
                    world=world,
                    stage=stage,
                    world_label=str(world),
                    single_stage=True,
                ))
                tasks.append(MarioTask(
                    env_id='SuperMarioBros{}-{}-v{}'.format(
                        world,
                        stage,
                        version,
                    ),
                    game='smb1',
                    game_family='smb1',
                    version=version,
                    rom_mode=rom_mode,
                    world=world,
                    stage=stage,
                    world_label=str(world),
                    single_stage=True,
                    alias_of=canonical_env_id,
                ))

    for version, rom_mode in enumerate(LOST_LEVELS_ROM_MODES):
        tasks.append(MarioTask(
            env_id='SuperMarioBros2-v{}'.format(version),
            game='lost_levels',
            game_family='lost_levels',
            version=version,
            rom_mode=rom_mode,
        ))
        for world in range(1, 14):
            world_label = _lost_levels_world_label(world)
            for stage in range(1, 5):
                tasks.append(MarioTask(
                    env_id='SuperMarioBros2-{}-{}-v{}'.format(
                        world_label,
                        stage,
                        version,
                    ),
                    game='lost_levels',
                    game_family='lost_levels',
                    version=version,
                    rom_mode=rom_mode,
                    world=world,
                    stage=stage,
                    world_label=world_label,
                    single_stage=True,
                ))

    tasks.append(MarioTask(
        env_id='SuperMarioBros2USA-v0',
        game='smb2_usa',
        game_family='smb2_usa',
        version=0,
        rom_mode='vanilla',
    ))
    for world, stage_count in enumerate(SMB2_USA_STAGES_PER_WORLD, start=1):
        for stage in range(1, stage_count + 1):
            tasks.append(MarioTask(
                env_id='SuperMarioBros2USA-{}-{}-v0'.format(world, stage),
                game='smb2_usa',
                game_family='smb2_usa',
                version=0,
                rom_mode='vanilla',
                world=world,
                stage=stage,
                world_label=str(world),
                single_stage=True,
            ))

    tasks.append(MarioTask(
        env_id='SuperMarioBros3-v0',
        game='smb3',
        game_family='smb3',
        version=0,
        rom_mode='vanilla',
    ))
    for world, stage in SMB3_VALIDATED_STAGES:
        tasks.append(MarioTask(
            env_id='SuperMarioBros3-{}-{}-v0'.format(world, stage),
            game='smb3',
            game_family='smb3',
            version=0,
            rom_mode='vanilla',
            world=world,
            stage=stage,
            world_label=str(world),
            single_stage=True,
        ))

    return tuple(tasks)


TASKS = _build_tasks()
_TASKS_BY_ENV_ID = {task.env_id: task for task in TASKS}


def all_tasks(
    *,
    include_aliases=False,
    game_family=None,
    rom_mode=None,
    single_stage=None,
    split=None,
    validated=None,
):
    """
    Return registered task metadata filtered for training/evaluation code.

    Args:
        include_aliases (bool): include alias environment IDs when True
        game_family (str): optional game-family filter
        rom_mode (str): optional ROM-mode filter
        single_stage (bool): optional single-stage/full-game filter
        split (str): optional "train" or "eval" split filter
        validated (bool): optional validated-coverage filter

    Returns:
        tuple[MarioTask]: matching tasks

    """
    tasks = TASKS
    if not include_aliases:
        tasks = tuple(task for task in tasks if task.alias_of is None)
    if game_family is not None:
        tasks = tuple(task for task in tasks if task.game_family == game_family)
    if rom_mode is not None:
        tasks = tuple(task for task in tasks if task.rom_mode == rom_mode)
    if single_stage is not None:
        tasks = tuple(task for task in tasks if task.single_stage == single_stage)
    if split == 'train':
        tasks = tuple(task for task in tasks if task.train_split)
    elif split == 'eval':
        tasks = tuple(task for task in tasks if task.eval_split)
    elif split is not None:
        raise ValueError("split must be one of: 'train', 'eval'")
    if validated is not None:
        tasks = tuple(task for task in tasks if task.validated == validated)
    return tasks


def task_ids(**filters):
    """Return matching task environment IDs for the given filters."""
    return tuple(task.env_id for task in all_tasks(**filters))


def task_for_env_id(env_id):
    """Return task metadata for a registered environment ID."""
    try:
        return _TASKS_BY_ENV_ID[env_id]
    except KeyError as exc:
        raise KeyError('unknown Mario environment ID: {}'.format(env_id)) from exc


def task_for_config(game, version, world=None, stage=None):
    """Return task metadata for a game/version/target tuple."""
    for task in TASKS:
        if task.alias_of is not None:
            continue
        if task.game != game:
            continue
        if task.version != version:
            continue
        if task.world != world or task.stage != stage:
            continue
        return task
    raise KeyError('no Mario task matches the requested configuration')


__all__ = [
    'LOST_LEVELS_ROM_MODES',
    'MarioTask',
    'SMB1_ROM_MODES',
    'SMB2_USA_STAGES_PER_WORLD',
    'SMB3_VALIDATED_STAGES',
    'TASKS',
    'all_tasks',
    'task_for_config',
    'task_for_env_id',
    'task_ids',
]
