import smb_env

class SuperMarioBrosEnvExplore(smb_env.SuperMarioBrosEnv):
    """This environment focuses on exploring the map for other ways to complete the level"""
    # Unlike the 'straight' environment, this environment only cares about completing the level fast
    # This makes Mario explore the map for ways to complete the level that might be faster
    def __init__(self, rom_mode='vanilla', lost_levels=False, target=None):
        super().__init__(rom_mode=rom_mode, lost_levels=lost_levels, target=target)

    @property
    def _time_reward(self):
        """Return the time reward for the current step"""
        time_diff = self.time - self.time_last
        self.time_last = self.time

        # the time can only increase if the game has been reset
        if time_diff > 0:
            return 0
        # put a slight encouragement to be completing the level as quickly as possible
        return -1 if time_diff > 0 else 1

    def _get_reward(self):
        """Return the reward after a step occurs."""
        return self._time_reward + self._death_penalty