"""Registration code of Gymnasium environments in this package."""
from .smb_env import SuperMarioBrosEnv
from .smb2_env import SuperMarioBros2Env
from .smb3_env import SuperMarioBros3Env
from .smb3_stages import SMB3Stage
from .smb3_stages import smb3_stage_matrix
from .tasks import MarioTask
from .tasks import all_tasks
from .tasks import task_for_env_id
from .tasks import task_ids
from ._registration import make


# define the outward facing API of this package
__all__ = [
    'make',
    'SuperMarioBrosEnv',
    'SuperMarioBros2Env',
    'SuperMarioBros3Env',
    'SMB3Stage',
    'smb3_stage_matrix',
    'MarioTask',
    'all_tasks',
    'task_for_env_id',
    'task_ids',
]
