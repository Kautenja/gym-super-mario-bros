"""Registration code of Gym environments in this package."""
from .smb_env import SuperMarioBrosEnv
from .smb_stage_env import SuperMarioBrosStageEnv
from ._registration import make


# define the outward facing API of this package
__all__ = [
    make.__name__,
    SuperMarioBrosEnv.__name__,
    SuperMarioBrosStageEnv.__name__,
]
