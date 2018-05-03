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

![smb](https://user-images.githubusercontent.com/2184469/39209488-854e960c-47cb-11e8-9e66-ddadcb0d7874.png)

An [OpenAI Gym](https://github.com/openai/gym) environment for
Super Mario Bros on the Nintendo Entertainment System (NES).

# Installation

The preferred installation of `gym-super-mario-bros` is from `pip`:

```shell
pip install gym-super-mario-bros
```

## NES Emulator

`gym-super-mario-bros` uses [FCEUX](http://www.fceux.com/web/home.html) to emulate NES games.
Make sure it's installed and in your `$PATH`.

### Unix

```shell
sudo apt-get install fceux
```

### Mac

```shell
brew install fceux
```

# Usage

```python
import gym_super_mario_bros
env = gym_super_mario_bros.make('SuperMarioBros-v0')

done = True
for step in range(5000):
    if done:
        state = env.reset()
    state, reward, done, info = env.step(env.action_space.sample())

env.close()
```

**NOTE:** `gym_super_mario_bros.make` is just an alias to `gym.make` for
convenience.

# Environments

These environments allow 3 attempts (lives) to make it through the 32 levels 
of the game. The environments only send reward-able game-play frames to 
agents; No cut-scenes, loading screens, etc. are sent from the NES emulator 
to an agent nor can an agent perform actions during these occurences. If a 
cut-scene is not able to be skipped by hacking the NES's RAM, the environment
will lock the Pyton process until the emulator is ready for the next action.

| Environment                    | Description                                      |
|:-------------------------------|:-------------------------------------------------|
| `SuperMarioBros-v0`            | 4 frames per action, standard ROM                |
| `SuperMarioBros-v1`            | 4 frames per action, custom down-sampled ROM     |
| `SuperMarioBrosNoFrameskip-v0` | 1 frame per action, standard ROM                 |
| `SuperMarioBrosNoFrameskip-v1` | 1 frame per action, custom down-sampled ROM      |

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
