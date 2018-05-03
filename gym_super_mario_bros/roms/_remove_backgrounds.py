"""A script that generates a new ROM with background colors removed."""


# read the original ROM from disk
with open('./super-mario-bros.nes', 'rb') as smb:
    rom = bytearray(smb.read())


# the color black
BLACK = 0x0d
# the memory locations to overwrite
BGS =  [0x005DF, 0x005E0, 0x005E1, 0x005E2, 0x005E3, 0x005E4, 0x005E5, 0x005E6]
for bg in BGS:
    rom[bg] = BLACK


# write the new ROM to disk
with open('./super-mario-bros-no-backgrounds.nes', 'wb') as smb:
    smb.write(rom)
