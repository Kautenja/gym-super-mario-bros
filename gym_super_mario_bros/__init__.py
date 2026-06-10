"""Registration code of Gymnasium environments in this package."""
from .smb_env import SuperMarioBrosEnv
from .smb2_env import SuperMarioBros2Env
from .smb3_env import SuperMarioBros3Env
from .smb_random_stages_env import SuperMarioBrosRandomStagesEnv
from ._registration import make


# define the outward facing API of this package
__all__ = [
    'make',
    'SuperMarioBrosEnv',
    'SuperMarioBros2Env',
    'SuperMarioBros3Env',
    'SuperMarioBrosRandomStagesEnv',
]
