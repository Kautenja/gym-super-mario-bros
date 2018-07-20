"""An OpenAI Gym environment for Super Mario Bros. and Lost Levels (levels)."""
from .smb_env import SuperMarioBrosEnv
from ._rom_mode import RomMode


class SuperMarioBrosEnvLevel(SuperMarioBrosEnv):
    """An environment for playing Super Mario Bros Levels with OpenAI Gym."""

    def __init__(self,
        rom_mode=RomMode.VANILLA,
        target_world=1,
        target_level=1,
        lost_levels=False,
    ):
        """
        Initialize a new Super Mario Bros environment.

        Args:
            rom_mode (RomMode): the ROM mode to use when loading ROMs from disk
            target_world (int): the world to target in the ROM
            target_level (int): the level to target in the given world
            lost_levels (bool): whether to load the ROM with lost levels.
                - False: load original Super Mario Bros.
                - True: load Super Mario Bros. Lost Levels

        Returns:
            None

        """
        # initialize the super object
        super(SuperMarioBrosEnvLevel, self).__init__(rom_mode, lost_levels)
        # Type and value check the target world parameter
        if not isinstance(target_world, int):
            raise TypeError('target_world must be of type: int')
        # TODO: value check _target_world

        # Type and value check the target level parameter
        if not isinstance(target_level, int):
            raise TypeError('target_level must be of type: int')
        # TODO: value check _target_level

        # setup target area if target world and level are specified
        target_area = target_level
        # setup the target area depending on whether this is SMB 1 or 2
        if lost_levels:
            # setup the target area depending on the target world and level
            if target_world in {1, 3}:
                if target_level >= 2:
                    target_area = target_area + 1
            elif target_world >= 5:
                # TODO: figure out why all worlds greater than 5 fail.
                # >=6 causes a change for
                target_area = target_area + 1
        else:
            # setup the target area depending on the target world and level
            if target_world in {1, 2, 4, 7}:
                if target_level >= 2:
                    target_area = target_area + 1

        self._target_world = target_world
        self._target_level = target_level
        self._target_area = target_area

    # MARK: RAM Hacks

    def _write_level(self):
        """Write the level data to RAM to overwrite the loading level."""
        self._write_mem(0x075f, self._target_world - 1)
        self._write_mem(0x075c, self._target_level - 1)
        self._write_mem(0x0760, self._target_area - 1)

    def _kill_mario(self):
        """Skip a death animation by forcing Mario to death."""
        # ignore the notion of lives. i.e. set the lives to 0
        self._write_mem(0x075a, 0)
        super(SuperMarioBrosEnvLevel, self)._kill_mario()

    def _skip_start_screen(self):
        # press and release the start button
        self._frame_advance(8)
        self._frame_advance(0)
        # Press start until the game starts
        while self._get_time() >= self._time_left:
            # update the local time counter
            self._time_left = self._get_time()
            # press the start button
            self._frame_advance(8)
            # force overwrite the level that is set to load
            self._write_level()
            # release the start button
            self._frame_advance(0)
            # run-out the prelevel timer to skip the animation
            self._runout_prelevel_timer()


# explicitly define the outward facing API of this module
__all__ = [SuperMarioBrosEnvLevel.__name__]
