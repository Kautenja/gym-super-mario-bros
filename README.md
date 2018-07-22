# gym-super-mario-bros

[![PackageVersion][pypi-version]][pypi-home]
[![PythonVersion][python-version]][python-home]
[![Stable][pypi-status]][pypi-home]
[![Format][pypi-format]][pypi-home]
[![License][pypi-license]](LICENSE)

[pypi-version]: https://badge.fury.io/py/gym-super-mario-bros.svg
[pypi-license]: https://img.shields.io/pypi/l/gym-super-mario-bros.svg
[pypi-status]: https://img.shields.io/pypi/status/gym-super-mario-bros.svg
[pypi-format]: https://img.shields.io/pypi/format/gym-super-mario-bros.svg
[pypi-home]: https://badge.fury.io/py/gym-super-mario-bros
[python-version]: https://img.shields.io/pypi/pyversions/gym-super-mario-bros.svg
[python-home]: https://python.org

![Mario](https://user-images.githubusercontent.com/2184469/40949613-7542733a-6834-11e8-895b-ce1cc3af9dbb.gif)

An [OpenAI Gym](https://github.com/openai/gym) environment for
Super Mario Bros. & Super Mario Bros. 2 (Lost Levels) on The Nintendo
Entertainment System (NES) using 
[the nes-py emulator](https://github.com/Kautenja/nes-py).

# Installation

The preferred installation of `gym-super-mario-bros` is from `pip`:

```shell
pip install gym-super-mario-bros
```

# Usage

## Python

You must import `gym_super_mario_bros` before trying to make an environment.
This is because gym environments are registered at runtime. By default, 
`gym_super_mario_bros` environments use the full NES action space of 256
discrete actions. To contstrain this, `gym_super_mario_bros.actions` provides
three actions lists (`RIGHT_ONLY`, `SIMPLE_MOVEMENT`, and `COMPLEX_MOVEMENT`)
for the `nes_py.wrappers.BinarySpaceToDiscreteSpaceEnv` wrapper. See 
[gym_super_mario_bros/actions.py](gym_super_mario_bros/actions.py) for a 
breakdown of the legal actions in each of these three lists.

```python
from nes_py.wrappers import BinarySpaceToDiscreteSpaceEnv
import gym_super_mario_bros
from gym_super_mario_bros.actions import SIMPLE_MOVEMENT
env = gym_super_mario_bros.make('SuperMarioBros-v0')
env = BinarySpaceToDiscreteSpaceEnv(env, SIMPLE_MOVEMENT)

done = True
for step in range(5000):
    if done:
        state = env.reset()
    state, reward, done, info = env.step(env.action_space.sample())
    env.render()

env.close()
```

**NOTE:** `gym_super_mario_bros.make` is just an alias to `gym.make` for
convenience.

**NOTE:** remove calls to `render` in training code for a nontrivial 
speedup.

## Command Line

`gym_super_mario_bros` feature a command line interface for playing
environments using either the keyboard, or uniform random movement.

```shell
gym_super_mario_bros -e <the environment ID to play> -m <`human` or `random`>
```

**NOTE:** by default, `-e` is set to `SuperMarioBros-v0` and `-m` is set to
`human`.

# Environments

These environments allow 3 attempts (lives) to make it through the 32 levels
of the game. The environments only send reward-able game-play frames to
agents; No cut-scenes, loading screens, etc. are sent from the NES emulator
to an agent nor can an agent perform actions during these occurrences. If a
cut-scene is not able to be skipped by hacking the NES's RAM, the environment
will lock the Python process until the emulator is ready for the next action.

| Environment                     | Game | Frameskip | ROM           | Screenshot |
|:--------------------------------|:-----|:----------|:--------------|:-----------|
| `SuperMarioBros-v0`             | SMB  | 4         | standard      | ![][v0]    |
| `SuperMarioBros-v1`             | SMB  | 4         | downsample    | ![][v1]    |
| `SuperMarioBros-v2`             | SMB  | 4         | pixel         | ![][v2]    |
| `SuperMarioBros-v3`             | SMB  | 4         | rectangle     | ![][v3]    |
| `SuperMarioBrosNoFrameskip-v0`  | SMB  | 1         | standard      | ![][v0]    |
| `SuperMarioBrosNoFrameskip-v1`  | SMB  | 1         | downsample    | ![][v1]    |
| `SuperMarioBrosNoFrameskip-v2`  | SMB  | 1         | pixel         | ![][v2]    |
| `SuperMarioBrosNoFrameskip-v3`  | SMB  | 1         | rectangle     | ![][v3]    |
| `SuperMarioBros2-v0`            | SMB2 | 4         | standard      | ![][2-v0]  |
| `SuperMarioBros2-v1`            | SMB2 | 4         | downsample    | ![][2-v1]  |
| `SuperMarioBros2NoFrameskip-v0` | SMB2 | 1         | standard      | ![][2-v0]  |
| `SuperMarioBros2NoFrameskip-v1` | SMB2 | 1         | downsample    | ![][2-v1]  |

[v0]: https://user-images.githubusercontent.com/2184469/40948820-3d15e5c2-6830-11e8-81d4-ecfaffee0a14.png
[v1]: https://user-images.githubusercontent.com/2184469/40948819-3cff6c48-6830-11e8-8373-8fad1665ac72.png
[v2]: https://user-images.githubusercontent.com/2184469/40948818-3cea09d4-6830-11e8-8efa-8f34d8b05b11.png
[v3]: https://user-images.githubusercontent.com/2184469/40948817-3cd6600a-6830-11e8-8abb-9cee6a31d377.png
[2-v0]: https://user-images.githubusercontent.com/2184469/40948822-3d3b8412-6830-11e8-860b-af3802f5373f.png
[2-v1]: https://user-images.githubusercontent.com/2184469/40948821-3d2d61a2-6830-11e8-8789-a92e750aa9a8.png

## Individual Levels

These environments allow a single attempt (life) to make it through a single
level of the game.

Use the template

    SuperMarioBros-<world>-<level>-v<version>

where:

-   `<world>` is a number in {1, 2, 3, 4, 5, 6, 7, 8} indicating the world
-   `<level>` is a number in {1, 2, 3, 4} indicating the level within a world
-   `<version>` is a number in {0, 1, 2, 3} specifying the ROM mode to use
    - 0: standard ROM
    - 1: downsampled ROM
    - 2: pixel ROM
    - 3: rectangle ROM
-   `NoFrameskip` can be added before the first hyphen to disable frame skip

For example, to play 4-2 on the downsampled ROM, you would use the environment
id `SuperMarioBros-4-2-v1`. To disable frame skip you would use
`SuperMarioBrosNoFrameskip-4-2-v1`.

# Citation

Please cite `gym-super-mario-bros` if you use it in your research.

```tex
@misc{gym-super-mario-bros,
  author = {Christian Kauten},
  title = {{S}uper {M}ario {B}ros for {O}pen{AI} {G}ym},
  year = {2018},
  publisher = {GitHub},
  howpublished = {\url{https://github.com/Kautenja/gym-super-mario-bros}},
}
```
