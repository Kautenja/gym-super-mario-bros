"""Registration code of Gym environments in this package."""
from .smb_env import SuperMarioBrosEnv
from ._registration import make
from .wrappers import wrap


def headless() -> None:
    """Set up the package for headless usage."""
    import os
    os.environ['SDL_VIDEODRIVER'] = 'dummy'


# define the outward facing API of this package
__all__ = [
    headless.__name__,
    make.__name__,
    SuperMarioBrosEnv.__name__,
    wrap.__name__,
]
