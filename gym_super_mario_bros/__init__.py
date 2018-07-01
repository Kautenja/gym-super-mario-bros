"""Registration code of Gym environments in this package."""
from ._registration import make
from .smb_env import SuperMarioBrosEnv
from .wrappers import wrap


# define the outward facing API of this package
__all__ = [
    make.__name__,
    SuperMarioBrosEnv.__name__,
    wrap.__name__,
]
