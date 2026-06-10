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
Bros. 2 (USA), and Super Mario Bros. 3 on The Nintendo Entertainment System
(NES) using
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
| `SuperMarioBros2-v0`            | SMB2 | standard      | ![][2-v0]  |
| `SuperMarioBros2USA-v0`         | SMB2 USA | standard  |            |
| `SuperMarioBros3-v0`            | SMB3 | standard      |            |

[v0]: https://user-images.githubusercontent.com/2184469/40948820-3d15e5c2-6830-11e8-81d4-ecfaffee0a14.png
[2-v0]: https://user-images.githubusercontent.com/2184469/40948822-3d3b8412-6830-11e8-860b-af3802f5373f.png

### Individual Stages

These environments allow a single attempt (life) to make it through a single
stage of the game.

Use the template

    SuperMarioBros-<world>-<stage>-v<version>

where:

-   `<world>` is a number in {1, 2, 3, 4, 5, 6, 7, 8} indicating the world
-   `<stage>` is a number in {1, 2, 3, 4} indicating the stage within a world
-   `<version>` is 0 for the standard ROM

For example, to play 4-2 on the standard ROM, you would use the environment
id `SuperMarioBros-4-2-v0`.

Super Mario Bros. 2 (USA) uses the vanilla ROM only. Use
`SuperMarioBros2USA-v0` for the full game, or the template

    SuperMarioBros2USA-<world>-<stage>-v0

where `<world>` is a number in {1, 2, 3, 4, 5, 6, 7}. Worlds 1 through 6 have
stages {1, 2, 3}; world 7 has stages {1, 2}.

Super Mario Bros. 3 uses the vanilla ROM only. Use `SuperMarioBros3-v0` for
the game, or `SuperMarioBros3-1-1-v0` for the validated World 1-1 single-stage
entry point.

## Step

Info about the rewards and info returned by the `step` method.

### Reward Function

The reward function combines dense progress with objective events. Progress is
rewarded only when the agent reaches a new best position for the attempt, so
tactical backtracking is not punished by the movement term. Score increases,
coins, cherries, powerups, health changes, level completion, time pressure, and
death penalties are then added when the underlying game exposes reliable RAM
counters for that title.

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

Newer SMB2 USA and SMB3 environments include additional game-specific keys
such as raw transition state, health, lives, map position, powerup timers,
P-meter state, invulnerability timers, and progress maxima where those values
are available from the ROM's RAM map.

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
