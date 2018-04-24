# NESGym - Super Mario Bros

![smb](https://user-images.githubusercontent.com/2184469/39209488-854e960c-47cb-11e8-9e66-ddadcb0d7874.png)

An [OpenAI Gym](https://github.com/openai/gym) environment for the original
Super Mario Bros. game on the Nintendo Entertainment System (NES). Built
using a fork of [NESGym](https://github.com/codescv/nesgym) and some snippets
from [gym-super-mario](https://github.com/ppaquette/gym-super-mario).

# Installation

The preferred installation of `nesgym-super-mario-bros` is from `pip`:

```shell
pip install nesgym-super-mario-bros
```

## NES Emulator

NESGym uses [FCEUX](http://www.fceux.com/web/home.html) to emulate NES games.
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

You _must_ import `nesgym_super_mario_bros` to register the environments with
gym before calling `gym.make('nesgym/SuperMarioBros-v0')`.

```python
import gym
# import nesgym_super_mario_bros to register environments with gym
import nesgym_super_mario_bros
env = gym.make('nesgym/SuperMarioBros-v0')

done = True
for step in range(5000):
    if done:
        state = env.reset()
    state, reward, done, info = env.step(env.action_space.sample())

env.close()
```
