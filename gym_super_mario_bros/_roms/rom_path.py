"""A method to load a ROM path."""
import os


def rom_path(lost_levels, rom_mode):
    """
    Return the ROM filename for a game and ROM mode.

    Args:
        lost_levels (bool): whether to use the lost levels ROM
        rom_mode (RomMode): the mode of the ROM hack to use

    Returns (str):
        the ROM path based on the input parameters

    """
    # Type and value check the lost levels parameter
    if not isinstance(lost_levels, bool):
        raise TypeError('lost_levels must be of type: bool')
    if lost_levels:
        if rom_mode == 'vanilla':
            rom = 'super-mario-bros-2.nes'
        elif rom_mode == 'pixel':
            raise ValueError('pixel_rom not supported for Lost Levels')
        elif rom_mode == 'rectangle':
            raise ValueError('rectangle_rom not supported for Lost Levels')
        elif rom_mode == 'downsample':
            rom = 'super-mario-bros-2-downsampled.nes'
        else:
            raise ValueError('rom_mode received invalid value')
    else:
        if rom_mode == 'vanilla':
            rom = 'super-mario-bros.nes'
        elif rom_mode == 'pixel':
            rom = 'super-mario-bros-pixel.nes'
        elif rom_mode == 'rectangle':
            rom = 'super-mario-bros-rect.nes'
        elif rom_mode == 'downsample':
            rom = 'super-mario-bros-downsampled.nes'
        else:
            raise ValueError('rom_mode received invalid value')
    # get the absolute path for the ROM
    rom = os.path.join(os.path.dirname(os.path.abspath(__file__)), rom)

    return rom


# explicitly define the outward facing API of this module
__all__ = [rom_path.__name__]
