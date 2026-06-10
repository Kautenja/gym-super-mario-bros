"""A method to load a ROM path."""
import os


# a dictionary mapping ROM paths first by lost levels, then by ROM hack mode
_ROM_PATHS = {
    # the dictionary of lost level ROM paths
    True: {
        'vanilla': 'super-mario-bros-lost-levels.nes',
        'downsample': 'super-mario-bros-lost-levels-downsample.nes',
    },
    # the dictionary of Super Mario Bros. 1 ROM paths
    False: {
        'vanilla': 'super-mario-bros.nes',
        'pixel': 'super-mario-bros-pixel.nes',
        'rectangle': 'super-mario-bros-rectangle.nes',
        'downsample': 'super-mario-bros-downsample.nes',
    }
}


_SUPER_MARIO_BROS_2_USA_ROM = 'super-mario-bros-2.nes'
_SUPER_MARIO_BROS_3_ROM = 'super-mario-bros-3.nes'


def rom_path(lost_levels, rom_mode):
    """
    Return the ROM filename for a game and ROM mode.

    Args:
        lost_levels (bool): whether to use the lost levels ROM
        rom_mode (str): the mode of the ROM hack to use as one of:
            - 'vanilla'
            - 'pixel'
            - 'downsample'
            - 'vanilla'

    Returns (str):
        the ROM path based on the input parameters

    """
    # Type and value check the lost levels parameter
    if not isinstance(lost_levels, bool):
        raise TypeError('lost_levels must be of type: bool')
    # try the unwrap the ROM path from the dictionary
    try:
        rom = _ROM_PATHS[lost_levels][rom_mode]
    except KeyError:
        raise ValueError('rom_mode ({}) not supported!'.format(rom_mode))
    # get the absolute path for the ROM
    rom = os.path.join(os.path.dirname(os.path.abspath(__file__)), rom)

    return rom


def smb2_rom_path():
    """
    Return the ROM filename for Super Mario Bros. 2 (USA).

    Returns (str):
        the absolute path to the Super Mario Bros. 2 (USA) ROM

    """
    return os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        _SUPER_MARIO_BROS_2_USA_ROM,
    )


def smb3_rom_path():
    """
    Return the ROM filename for Super Mario Bros. 3.

    Returns (str):
        the absolute path to the Super Mario Bros. 3 ROM

    """
    return os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        _SUPER_MARIO_BROS_3_ROM,
    )


# explicitly define the outward facing API of this module
__all__ = [
    rom_path.__name__,
    smb2_rom_path.__name__,
    smb3_rom_path.__name__,
]
