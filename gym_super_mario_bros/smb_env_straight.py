import smb_env
class SuperMarioBrosEnvStraight(smb_env.SuperMarioBrosEnv):
    """This environment focuses on just getting Mario form the start of the level to the end of level
    in the 'traditional' way which is going from the right of the map to left of map whilst trying not to die"""

    def __init__(self, rom_mode='vanilla', lost_levels=False, target=None):
        super().__init__(rom_mode=rom_mode, lost_levels=lost_levels, target=target)


    @property
    def _x_reward(self):
        """Return the reward for Mario moving in the correct direction"""
        # encourage to move to the right
        x_diff = self.x - self.x_last
        self.x_last = self.x
        # when the game resets, Mario's x position drastically drops
        return x_diff if x_diff > -5 else 0

    @property
    def _time_reward(self):
        """Return the time reward for the current step"""
        time_diff = self.time - self.time_last
        self.time_last = self.time

        # the time can only increase if the game has been reset
        if time_diff > 0:
            return 0
        # encourage to complete the level as quickly as possible
        # if the time has decreased, punish the agent. Otherwise, reward it
        return -1 if time_diff > 0 else 1



    def _get_reward(self):
        """Return the reward after a step occurs."""
        return self._x_reward + self._time_reward + self._death_penalty




