"""Registration code of Gym environments in this package."""
from .smb_env import SuperMarioBrosEnv


# define the outward facing API of this package
__all__ = [
    SuperMarioBrosEnv.__name__,
]
