# NESGym - Super Mario Bros

An openai-gym wrapper for the NES game, Super Mario Bros built using a fork
of [NESGym](https://github.com/codescv/nesgym) and some snippets from
[gym-super-mario](https://github.com/ppaquette/gym-super-mario).

# Installation

## NES Emulator

NESGym uses FCEUX to emulate NES games. Make sure it's installed and in your
`$PATH`.

### Unix

```shell
sudo apt-get install fceux
```

### Mac

```shell
brew install fceux
```

# Usage

You _must_ import `nesgym` to register the environments with gym before
calling `gym.make('nesgym/SuperMarioBros-v0')`. The action `4` used below
holds right so Mario will move in an infinite loop.

```python
import gym
# import nesgym to register environments with gym
import nesgym
env = gym.make('nesgym/SuperMarioBros-v0')

done = True
for step in range(5000):
    if done:
        obs = env.reset()
    obs, reward, done, info = env.step(4)
```
