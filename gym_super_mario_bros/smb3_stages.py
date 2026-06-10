"""Stage metadata for Super Mario Bros. 3."""
from dataclasses import dataclass


SMB3_STAGES_PER_WORLD = (6, 5, 9, 6, 9, 10, 9, 2)
SMB3_VALIDATED_STAGES = ((1, 1), (1, 2), (1, 4), (1, 6))


@dataclass(frozen=True)
class SMB3Stage:
    """A catalog entry for one numbered Super Mario Bros. 3 course."""

    world: int
    stage: int
    validated: bool = False

    @property
    def env_id(self):
        """Return the registered-style environment ID for this stage."""
        return 'SuperMarioBros3-{}-{}-v0'.format(self.world, self.stage)

    @property
    def target(self):
        """Return the ``SuperMarioBros3Env`` target tuple for this stage."""
        return self.world, self.stage

    @property
    def world_label(self):
        """Return the public world label."""
        return str(self.world)


def _build_smb3_stage_matrix():
    """Return catalog entries for SMB3's numbered courses."""
    validated = set(SMB3_VALIDATED_STAGES)
    stages = []
    for world, stage_count in enumerate(SMB3_STAGES_PER_WORLD, start=1):
        for stage in range(1, stage_count + 1):
            stages.append(SMB3Stage(
                world=world,
                stage=stage,
                validated=(world, stage) in validated,
            ))
    return tuple(stages)


SMB3_STAGE_MATRIX = _build_smb3_stage_matrix()


def smb3_stage_matrix(*, validated=None):
    """
    Return catalog metadata for SMB3 numbered courses.

    Args:
        validated (bool): optionally filter to stages with validated reset
            entry recipes.

    Returns:
        tuple[SMB3Stage]: matching SMB3 stage metadata

    """
    stages = SMB3_STAGE_MATRIX
    if validated is not None:
        stages = tuple(stage for stage in stages if stage.validated == validated)
    return stages


__all__ = [
    'SMB3Stage',
    'SMB3_STAGES_PER_WORLD',
    'SMB3_STAGE_MATRIX',
    'SMB3_VALIDATED_STAGES',
    'smb3_stage_matrix',
]
