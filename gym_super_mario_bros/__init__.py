"""Registration code of Gym environments in this package."""
from .smb_env import SuperMarioBrosEnv
from ._registration import make


# define the outward facing API of this package
__all__ = [
    make.__name__,
    SuperMarioBrosEnv.__name__,
]
