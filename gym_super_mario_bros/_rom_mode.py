"""An enumeration of valid ROM hacks to load into the emulator."""
import enum


@enum.unique
class RomMode(enum.Enum):
    """An enumeration of valid ROM hacks to load into the emulator."""
    # the standard ROM with no modifications
    VANILLA = 0
    # down-sampled ROM with static artifacts removed
    DOWNSAMPLE = 1
    # a simpler pixelated version of graphics
    PIXEL = 2
    # an even simpler rectangular version of graphics
    RECTANGLE = 3


# explicitly define the outward facing API of this module
__all__ = [RomMode.__name__]
