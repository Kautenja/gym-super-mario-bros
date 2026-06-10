"""Methods to load packaged ROM paths."""
import os


_SUPER_MARIO_BROS_ROM = 'super-mario-bros.nes'
_SUPER_MARIO_BROS_2_JP_ROM = 'super-mario-bros-lost-levels.nes'
_SUPER_MARIO_BROS_2_USA_ROM = 'super-mario-bros-2.nes'
_SUPER_MARIO_BROS_3_ROM = 'super-mario-bros-3.nes'


def _rom_path(filename):
    """Return the absolute path to a packaged ROM file."""
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)


def smb1_rom_path():
    """
    Return the ROM filename for Super Mario Bros.

    Returns (str):
        the absolute path to the Super Mario Bros. ROM

    """
    return _rom_path(_SUPER_MARIO_BROS_ROM)


def smb2jp_rom_path():
    """
    Return the ROM filename for Super Mario Bros. 2 (Japan / Lost Levels).

    Returns (str):
        the absolute path to the Super Mario Bros. 2 (Japan) ROM

    """
    return _rom_path(_SUPER_MARIO_BROS_2_JP_ROM)


def smb2_rom_path():
    """
    Return the ROM filename for Super Mario Bros. 2 (USA).

    Returns (str):
        the absolute path to the Super Mario Bros. 2 (USA) ROM

    """
    return _rom_path(_SUPER_MARIO_BROS_2_USA_ROM)


def smb3_rom_path():
    """
    Return the ROM filename for Super Mario Bros. 3.

    Returns (str):
        the absolute path to the Super Mario Bros. 3 ROM

    """
    return _rom_path(_SUPER_MARIO_BROS_3_ROM)


# explicitly define the outward facing API of this module
__all__ = [
    smb1_rom_path.__name__,
    smb2jp_rom_path.__name__,
    smb2_rom_path.__name__,
    smb3_rom_path.__name__,
]
