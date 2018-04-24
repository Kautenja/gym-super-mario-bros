# NESGym

An openai-gym wrapper for nes games.

# Installation
- Install nes emulator and make sure `fceux` is in your $PATH. In ubuntu, simple use `apt install fceux`.
- Copy state files from `roms/fcs/*` to your `~/.fceux/fcs/``

# Example usage
```python
# import nesgym to register environments to gym
import nesgym
env = gym.make('nesgym/NekketsuSoccerPK-v0')
obs = env.reset()

for step in range(10000):
  action = env.action_space.sample()
  obs, reward, done, info = env.step(action)

```

# Examples for training dqn
An implementation of dqn is in src/dqn.
You can train dqn model for atari and nes with `run-atari.py` and `run-soccer.py`, respectively.

# Integrating new nes games
You need two files: a lua interface file, and an openai gym environment class(python) file.
The lua file needs to get the reward from emulator(typically extracting from a memory location), and the python file defines the game specific environment.
For an example of lua file, see `src/lua/soccer.lua`; for an example of gym env file, see `src/nesgym/nekketsu_soccer_env.py`.

# Gallery
## training atari games
![atari](images/atari.png)

## training fc games
![fc-soccer](images/soccer.png)
