"""Remove background colors from a Super Mario Bros ROM.

    python _remove_backgrounds.py <Original ROM> <Output ROM>
"""
import sys


# load the input and output file names from the command line
try:
    input_file = sys.argv[1]
    output_file = sys.argv[2]
except IndexError:
    # missing arguments, print documentation and exit
    print(__doc__)
    sys.exit(-1)


# read the original ROM from disk
with open(input_file, 'rb') as smb:
    rom = bytearray(smb.read())


# the color black
BLACK = 0x0d
# the memory locations to overwrite
BGS =  [
    0x005DF,
    0x005E0,
    0x005E1,
    0x005E2,
    0x005E3,
    0x005E4,
    0x005E5,
    0x005E6
]
# iterate over the memory addresses of colors to overwrite and set to black
for bg in BGS:
    rom[bg] = BLACK


# write the new ROM to disk
with open(output_file, 'wb') as smb:
    smb.write(rom)
