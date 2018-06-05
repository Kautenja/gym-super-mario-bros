"""Registration code of Gym environments in this package."""
from .smb_env import SuperMarioBrosEnv
from ._registration import make
from .wrappers import wrap


# define the outward facing API of this module (none, gym provides the API)
__all__ = [
    SuperMarioBrosEnv.__name__,
    make.__name__,
    wrap.__name__,
]
