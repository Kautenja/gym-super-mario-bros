"""An OpenAI Gym environment for Super Mario Bros. and Lost Levels (levels)."""
from .smb_env import SuperMarioBrosEnv
from ._rom_mode import RomMode


class SuperMarioBrosLevelEnv(SuperMarioBrosEnv):
    """An environment for playing Super Mario Bros Levels with OpenAI Gym."""

    def __init__(self,
        frameskip=1,
        max_episode_steps=float('inf'),
        rom_mode=RomMode.VANILLA,
        lost_levels=False,
        target_world=1,
        target_level=1,
    ):
        """
        Initialize a new Super Mario Bros environment.

        Args:
            frameskip (int): the number of frames to skip between steps
            max_episode_steps (float): number of steps before an episode ends
            rom_mode (RomMode): the ROM mode to use when loading ROMs from disk
            lost_levels (bool): whether to load the ROM with lost levels.
                - False: load original Super Mario Bros.
                - True: load Super Mario Bros. Lost Levels
            target_world (int): the world to target in the ROM
            target_level (int): the level to target in the given world

        Returns:
            None

        """
        # Type and value check the target world parameter
        if not isinstance(target_world, int):
            raise TypeError('target_world must be of type: int')
        if lost_levels:
            if target_world > 12:
                worlds = set(range(1, 12 + 1))
                raise ValueError('target_world')
        elif target_world > 8:
            worlds = set(range(1, 8 + 1))
            raise ValueError('target_world must be in '.format(worlds))

        # Type and value check the target level parameter
        if not isinstance(target_level, int):
            raise TypeError('target_level must be of type: int')
        if target_level > 4:
            levels = set(range(1, 4 + 1))
            raise ValueError('target_level must be in '.format(levels))

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
                # target_area = target_area + 1
                # for now just raise a value error
                worlds = set(range(5, 12 + 1))
                msg = 'lost levels worlds {} not supported'.format(worlds)
                raise ValueError(msg)
        else:
            # setup the target area depending on the target world and level
            if target_world in {1, 2, 4, 7}:
                if target_level >= 2:
                    target_area = target_area + 1

        # copy the values to local instance variables
        self._target_world = target_world
        self._target_level = target_level
        self._target_area = target_area

        # initialize the super object
        super(SuperMarioBrosLevelEnv, self).__init__(
            frameskip=frameskip,
            max_episode_steps=max_episode_steps,
            rom_mode=rom_mode,
            lost_levels=lost_levels,
        )

    # MARK: RAM Hacks

    def _write_level(self):
        """Write the level data to RAM to overwrite the loading level."""
        self._write_mem(0x075f, self._target_world - 1)
        self._write_mem(0x075c, self._target_level - 1)
        self._write_mem(0x0760, self._target_area - 1)

    def _skip_start_screen(self):
        # press and release the start button
        self._frame_advance(8)
        self._frame_advance(0)
        # Press start until the game starts
        while self._get_time() == 0:
            # press the start button
            self._frame_advance(8)
            # force overwrite the level that is set to load
            self._write_level()
            # release the start button
            self._frame_advance(0)
            # run-out the prelevel timer to skip the animation
            self._runout_prelevel_timer()
        # after the start screen idle to skip some extra frames
        while self._get_time() >= self._time_left:
            self._time_left = self._get_time()
            self._frame_advance(8)
            self._frame_advance(0)

    def _get_done(self):
        """Return True if the episode is over, False otherwise."""
        return (
            self._get_is_dying() or
            self._get_is_dead() or
            self._get_is_world_over() or
            self._get_is_level_over()
        )


# explicitly define the outward facing API of this module
__all__ = [SuperMarioBrosLevelEnv.__name__]
