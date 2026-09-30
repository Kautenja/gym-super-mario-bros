# gym-super-mario-bros Licensing

The original project code uses the MIT License. Nintendo game ROMs are excluded
from that grant. The standard license text is in [LICENSE](LICENSE), separate
from this scope guide so GitHub can detect the software license.

## Original Code And Documentation

Copyright (c) 2018 Christian Kauten. Existing contributor notices remain in
effect.

The MIT License applies to the original Python source, tests, development
scripts, workflow configuration, and documentation in this repository. This
includes the Python helpers in `gym_super_mario_bros/_roms/`, but excludes the
`.nes` game files in that directory.

The current MIT grant replaces the former custom educational-purpose notice
for the original project materials. Educational and research use remains a
project goal, rather than an additional restriction on the MIT-licensed code.

## Nintendo Game Assets

The bundled Super Mario Bros., Super Mario Bros. 2 (Lost Levels), Super Mario
Bros. 2 (USA), and Super Mario Bros. 3 ROMs are third-party game assets. They
are not licensed under MIT by this project. Their copyright and other rights
remain with Nintendo and the respective rights holders; inclusion in this
repository does not grant permission to copy, modify, or redistribute them.
See [the ROM notice](docs/licenses/Nintendo-ROMs.txt) for the covered files.

This project is not affiliated with nor approved by Nintendo Co., Ltd. The
software license does not grant rights to Nintendo's names, trademarks,
characters, game artwork, or audio.

## Dependencies And Distribution Metadata

Dependencies such as [nes-py](https://github.com/Kautenja/nes-py) and
[Gymnasium](https://github.com/Farama-Foundation/Gymnasium) retain their own
licenses. Installing them does not change the terms of this project's code
or the game assets.

GitHub's detected MIT license describes the original project code. Python
distributions also contain the ROM files, so [pyproject.toml](pyproject.toml)
uses `MIT AND LicenseRef-Nintendo-ROMs` to distinguish the code license from
the excluded assets. `LicenseRef-Nintendo-ROMs` refers to the bundled ROM
notice; it records the absence of a license grant from this project for those
files, rather than granting additional rights. These are separate scopes,
not alternative licenses for all files.

Source and wheel distributions include `LICENSE`, this scope guide, and the
ROM notice through the `license-files` configuration. Keep all three together
when distributing the package, and preserve applicable third-party notices.
