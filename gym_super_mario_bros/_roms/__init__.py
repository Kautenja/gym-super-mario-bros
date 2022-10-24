"""Methods for ROM file management."""
from .decode_target import decode_target
from .rom_path import rom_path


# explicitly define the outward facing API of this package
__all__ = [
    decode_target.__name__,
    rom_path.__name__,
]
