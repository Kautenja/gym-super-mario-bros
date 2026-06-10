# gym-super-mario-bros

[![BuildStatus][build-status]][ci-server]
[![PackageVersion][pypi-version]][pypi-home]
[![PythonVersion][python-version]][python-home]
[![Stable][pypi-status]][pypi-home]
[![Format][pypi-format]][pypi-home]
[![License][pypi-license]](LICENSE)

[build-status]: https://github.com/Kautenja/gym-super-mario-bros/actions/workflows/ci.yml/badge.svg?branch=master
[ci-server]: https://github.com/Kautenja/gym-super-mario-bros/actions/workflows/ci.yml
[pypi-version]: https://badge.fury.io/py/gym-super-mario-bros.svg
[pypi-license]: https://img.shields.io/pypi/l/gym-super-mario-bros.svg
[pypi-status]: https://img.shields.io/pypi/status/gym-super-mario-bros.svg
[pypi-format]: https://img.shields.io/pypi/format/gym-super-mario-bros.svg
[pypi-home]: https://badge.fury.io/py/gym-super-mario-bros
[python-version]: https://img.shields.io/pypi/pyversions/gym-super-mario-bros.svg
[python-home]: https://python.org

![Mario](https://user-images.githubusercontent.com/2184469/40949613-7542733a-6834-11e8-895b-ce1cc3af9dbb.gif)

A [Gymnasium](https://gymnasium.farama.org/) environment for
Super Mario Bros., Super Mario Bros. 2 (Lost Levels), and Super Mario
Bros. 2 (USA) on The Nintendo Entertainment System (NES) using
[the nes-py emulator](https://github.com/Kautenja/nes-py).

`gym-super-mario-bros` targets Gymnasium's modern reset, step, render-mode,
and truncation semantics. It currently supports CPython 3.13 and 3.14 in CI.

## Installation

The preferred installation of `gym-super-mario-bros` is from `pip`:

```shell
pip install gym-super-mario-bros
```

Python 3.13 or newer is required. The supported CI targets are CPython 3.13
and 3.14.

Because `gym-super-mario-bros` depends on the native `nes-py` emulator, Linux
`GLIBCXX_*` loader errors and Windows compiler-toolchain failures are usually
`nes-py` installation/runtime issues rather than wrapper bugs. See the
[`nes-py` installation notes](https://github.com/Kautenja/nes-py#installation)
for the current compiler and runtime expectations.

## Usage

### Python

You must import `gym_super_mario_bros` before trying to make an environment.
This is because Gymnasium environments are registered at runtime. By default,
`gym_super_mario_bros` environments use the full NES action space of 256
discrete actions. To constrain this, `gym_super_mario_bros.actions` provides
three actions lists (`RIGHT_ONLY`, `SIMPLE_MOVEMENT`, and `COMPLEX_MOVEMENT`)
for the `nes_py.wrappers.JoypadSpace` wrapper. See
[gym_super_mario_bros/actions.py](https://github.com/Kautenja/gym-super-mario-bros/blob/master/gym_super_mario_bros/actions.py) for a
breakdown of the legal actions in each of these three lists.

```python
import gymnasium as gym
from nes_py.wrappers import JoypadSpace
import gym_super_mario_bros
from gym_super_mario_bros.actions import SIMPLE_MOVEMENT

env = gym.make('SuperMarioBros-v0', render_mode='human')
env = JoypadSpace(env, SIMPLE_MOVEMENT)

done = True
for step in range(5000):
    if done:
        state, info = env.reset(seed=123)
    state, reward, terminated, truncated, info = env.step(env.action_space.sample())
    done = terminated or truncated
    env.render()

env.close()
```

**NOTE:** `gym_super_mario_bros.make` is just an alias to `gymnasium.make` for
convenience after `gym_super_mario_bros` is imported.

**NOTE:** registered environments use Gymnasium's `TimeLimit` wrapper with
`max_episode_steps=9999999` to preserve the historical cap while allowing the
game logic to end normal episodes with `terminated=True`. Passing a shorter
`max_episode_steps` to `gymnasium.make()` is the supported way to test or train
with external time truncation, which returns `truncated=True`.

**NOTE:** remove calls to `render` in training code for a nontrivial
speedup.

### Command Line

`gym_super_mario_bros` features a command line interface for playing
environments using either the keyboard, or uniform random movement.

```shell
python -m gym_super_mario_bros --env <environment ID> --mode <human|random>
gym_super_mario_bros --env <environment ID> --mode <human|random>
```

**NOTE:** by default, `-e` is set to `SuperMarioBros-v0` and `-m` is set to
`human`, `--actionspace/-a` is set to `nes`, and rendering is enabled.

Human keyboard play opens a graphical window:

```shell
gym_super_mario_bros --env SuperMarioBros-v0 --mode human --actionspace simple
```

Random play can be rendered or run headlessly. Use `--seed` to seed the first
environment reset:

```shell
gym_super_mario_bros --mode random --steps 1000 --no-render --seed 123
```

Use `--actionspace/-a` to select `nes`, `right`, `simple`, or `complex`.
Human mode requires rendering, so `--mode human --no-render` is rejected.

Print the CLI help with:

```shell
python -m gym_super_mario_bros --help
```

**NOTE:** `SuperMarioBrosRandomStages-*` support the `--stages/-S` flag for
supplying the set of stages to sample from like `-S 1-4 2-4 3-4 4-4`.

## Environments

These environments allow 3 attempts (lives) to make it through the 32 stages
in the game. The environments only send reward-able game-play frames to
agents; No cut-scenes, loading screens, etc. are sent from the NES emulator
to an agent nor can an agent perform actions during these instances. If a
cut-scene is not able to be skipped by hacking the NES's RAM, the environment
will lock the Python process until the emulator is ready for the next action.

| Environment                     | Game | ROM           | Screenshot |
|:--------------------------------|:-----|:--------------|:-----------|
| `SuperMarioBros-v0`             | SMB  | standard      | ![][v0]    |
| `SuperMarioBros-v1`             | SMB  | downsample    | ![][v1]    |
| `SuperMarioBros-v2`             | SMB  | pixel         | ![][v2]    |
| `SuperMarioBros-v3`             | SMB  | rectangle     | ![][v3]    |
| `SuperMarioBros2-v0`            | SMB2 | standard      | ![][2-v0]  |
| `SuperMarioBros2-v1`            | SMB2 | downsample    | ![][2-v1]  |
| `SuperMarioBros2USA-v0`         | SMB2 USA | standard  |            |

[v0]: https://user-images.githubusercontent.com/2184469/40948820-3d15e5c2-6830-11e8-81d4-ecfaffee0a14.png
[v1]: https://user-images.githubusercontent.com/2184469/40948819-3cff6c48-6830-11e8-8373-8fad1665ac72.png
[v2]: https://user-images.githubusercontent.com/2184469/40948818-3cea09d4-6830-11e8-8efa-8f34d8b05b11.png
[v3]: https://user-images.githubusercontent.com/2184469/40948817-3cd6600a-6830-11e8-8abb-9cee6a31d377.png
[2-v0]: https://user-images.githubusercontent.com/2184469/40948822-3d3b8412-6830-11e8-860b-af3802f5373f.png
[2-v1]: https://user-images.githubusercontent.com/2184469/40948821-3d2d61a2-6830-11e8-8789-a92e750aa9a8.png

### Individual Stages

These environments allow a single attempt (life) to make it through a single
stage of the game.

Use the template

    SuperMarioBros-<world>-<stage>-v<version>

where:

-   `<world>` is a number in {1, 2, 3, 4, 5, 6, 7, 8} indicating the world
-   `<stage>` is a number in {1, 2, 3, 4} indicating the stage within a world
-   `<version>` is a number in {0, 1, 2, 3} specifying the ROM mode to use
    - 0: standard ROM
    - 1: downsampled ROM
    - 2: pixel ROM
    - 3: rectangle ROM

For example, to play 4-2 on the downsampled ROM, you would use the environment
id `SuperMarioBros-4-2-v1`.

Super Mario Bros. 2 (USA) uses the vanilla ROM only. Use
`SuperMarioBros2USA-v0` for the full game, or the template

    SuperMarioBros2USA-<world>-<stage>-v0

where `<world>` is a number in {1, 2, 3, 4, 5, 6, 7}. Worlds 1 through 6 have
stages {1, 2, 3}; world 7 has stages {1, 2}.

### Random Stage Selection

The random stage selection environment randomly selects a stage and allows a
single attempt to clear it. Upon a death and subsequent call to `reset` the
environment randomly selects a new stage. This is only available for the
standard Super Mario Bros. game, _not_ Lost Levels (at the moment). To use
these environments, append `RandomStages` to the `SuperMarioBros` id. For
example, to use the standard ROM with random stage selection use
`SuperMarioBrosRandomStages-v0`. To seed the random stage selection pass the
`seed` keyword argument to the `reset` method directly like `reset(seed=222)`.

In addition to randomly selecting any of the 32 original stages, a subset of
user-defined stages can be specified to limit the random choice of stages to a
specific subset. For example, the stage selector could be limited to only
sample castle stages, water levels, underground, and more.

To specify a default subset of stages to randomly sample from, create a list
of each stage to allow to be sampled and pass that list to the `gymnasium.make()`
function. For example:

```python
gym.make('SuperMarioBrosRandomStages-v0', stages=['1-4', '2-4', '3-4', '4-4'])
```

The example above will sample a random stage from 1-4, 2-4, 3-4, and 4-4 upon
every call to `reset`. A reset call can also override the subset for one
episode:

```python
state, info = env.reset(seed=222, options={'stages': ['4-2']})
```

## Step

Info about the rewards and info returned by the `step` method.

### Reward Function

The reward function assumes the objective of the game is to move as far right
as possible (increase the agent's _x_ value), as fast as possible, without
dying. To model this game, three separate variables compose the reward:

1.  _v_: the difference in agent _x_ values between states
    -   in this case this is instantaneous velocity for the given step
    -   _v = x1 - x0_
        -   _x0_ is the x position before the step
        -   _x1_ is the x position after the step
    -   moving right ⇔ _v > 0_
    -   moving left ⇔ _v < 0_
    -   not moving ⇔ _v = 0_
2.  _c_: the difference in the game clock between frames
    -   the penalty prevents the agent from standing still
    -   _c = c0 - c1_
        -   _c0_ is the clock reading before the step
        -   _c1_ is the clock reading after the step
    -   no clock tick ⇔ _c = 0_
    -   clock tick ⇔ _c < 0_
3.  _d_: a death penalty that penalizes the agent for dying in a state
    -   this penalty encourages the agent to avoid death
    -   alive ⇔ _d = 0_
    -   dead ⇔ _d = -15_

_r = v + c + d_

The reward is clipped into the range _(-15, 15)_.

### `info` dictionary

The `info` dictionary returned by the `step` method contains the following
keys:

| Key        | Type   | Description
|:-----------|:-------|:------------------------------------------------------|
| `coins   ` | `int`  | The number of collected coins
| `flag_get` | `bool` | True if Mario reached a flag or ax
| `life`     | `int`  | The number of lives left, i.e., _{3, 2, 1}_
| `score`    | `int`  | The cumulative in-game score
| `stage`    | `int`  | The current stage, i.e., _{1, ..., 4}_
| `status`   | `str`  | Mario's status, i.e., _{'small', 'tall', 'fireball'}_
| `time`     | `int`  | The time left on the clock
| `world`    | `int`  | The current world, i.e., _{1, ..., 8}_
| `x_pos`    | `int`  | Mario's _x_ position in the stage (from the left)
| `y_pos`    | `int`  | Mario's _y_ position in the stage (from the bottom)

## Publishing

PyPI releases are published by the `Publish to PyPI` GitHub Actions workflow
through PyPI trusted publishing, not by local `twine` credentials. Configure
the PyPI project publisher with owner `Kautenja`, repository
`gym-super-mario-bros`, workflow filename `publish.yml`, and environment
`pypi`. Publish a release by pushing a tag that matches `pyproject.toml`'s
version, with or without a leading `v`, and then creating the corresponding
GitHub release so the workflow can build and upload the distribution artifacts.

## Citation

Please cite `gym-super-mario-bros` if you use it in your research.

```tex
@misc{gym-super-mario-bros,
  author = {Christian Kauten},
  howpublished = {GitHub},
  title = {{S}uper {M}ario {B}ros for {O}pen{AI} {G}ym},
  URL = {https://github.com/Kautenja/gym-super-mario-bros},
  year = {2018},
}
```
