"""A Gymnasium environment for Super Mario Bros. 2 (USA)."""
from nes_py import NESEnv
from ._roms import smb2_rom_path


_CHARACTER_MAP = {
    0: 'mario',
    1: 'princess',
    2: 'toad',
    3: 'luigi',
}


_STAGES_PER_WORLD = (3, 3, 3, 3, 3, 3, 2)


_LEVEL_TRANSITION_RESTART = 0x01
_LEVEL_TRANSITION_GAME_OVER = 0x02
_LEVEL_TRANSITION_COMPLETE = 0x03
_LEVEL_TRANSITION_WARP = 0x04


def _decode_smb2_target(target):
    """
    Return the target world, stage, and linear level index.

    Args:
        target (None, tuple): the optional (world, stage) target

    Returns:
        a tuple of (world, stage, level index)

    """
    if target is None:
        return None, None, None
    if not isinstance(target, tuple):
        raise TypeError('target must be of type tuple')

    target_world, target_stage = target
    if not isinstance(target_world, int):
        raise TypeError('target_world must be of type: int')
    if not 1 <= target_world <= len(_STAGES_PER_WORLD):
        raise ValueError('target_world must be in {1, ..., 7}')

    if not isinstance(target_stage, int):
        raise TypeError('target_stage must be of type: int')
    max_stage = _STAGES_PER_WORLD[target_world - 1]
    if not 1 <= target_stage <= max_stage:
        raise ValueError(
            'target_stage must be in {1, ..., %d}' % max_stage
        )

    target_level = sum(_STAGES_PER_WORLD[:target_world - 1])
    target_level += target_stage - 1
    return target_world, target_stage, target_level


def _decode_smb2_level(level):
    """
    Return the public world and stage for a zero-based SMB2 level index.

    Args:
        level (int): the zero-based level index from RAM

    Returns:
        a tuple of (world, stage)

    """
    level = max(0, min(int(level), sum(_STAGES_PER_WORLD) - 1))
    for world, stage_count in enumerate(_STAGES_PER_WORLD, start=1):
        if level < stage_count:
            return world, level + 1
        level -= stage_count
    return 7, 2


class SuperMarioBros2Env(NESEnv):
    """An environment for playing Super Mario Bros. 2 (USA)."""

    # the legal range of rewards for each step
    reward_range = (-15, 15)

    def __init__(self, target=None, render_mode=None):
        """
        Initialize a new Super Mario Bros. 2 (USA) environment.

        Args:
            target (tuple): a tuple of the (world, stage) to play as a level
            render_mode (str): the render mode to use, if any

        Returns:
            None

        """
        rom = smb2_rom_path()
        super(SuperMarioBros2Env, self).__init__(rom, render_mode=render_mode)
        target = _decode_smb2_target(target)
        self._target_world, self._target_stage, self._target_level = target
        self._x_position_last = 0
        self.reset()
        self._skip_start_screen()
        self._backup()

    @property
    def is_single_stage_env(self):
        """Return True if this environment is a stage environment."""
        return self._target_level is not None

    # MARK: Memory access

    def _read_mem(self, address):
        """Read one RAM byte as a Python integer."""
        return int(self.ram[address])

    @property
    def _level(self):
        """Return the current linear level index."""
        return self._read_mem(0x0531)

    @property
    def _world(self):
        """Return the current world (1 to 7)."""
        return _decode_smb2_level(self._level)[0]

    @property
    def _stage(self):
        """Return the current stage within the world."""
        return _decode_smb2_level(self._level)[1]

    @property
    def _lives(self):
        """Return the raw total life count, including the current life."""
        return self._read_mem(0x04ed)

    @property
    def _life(self):
        """Return the displayed extra lives count."""
        if self._lives == 0xff:
            return 0
        return max(self._lives - 1, 0)

    @property
    def _coins(self):
        """Return the number of coins pulled in subspace."""
        return self._read_mem(0x062b)

    @property
    def _cherries(self):
        """Return the number of collected cherries."""
        return self._read_mem(0x062a)

    @property
    def _character(self):
        """Return the selected character name."""
        return _CHARACTER_MAP.get(self._read_mem(0x008f), 'unknown')

    @property
    def _health(self):
        """Return the current number of hearts."""
        health = self._read_mem(0x04c2)
        if health == 0:
            return 0
        return (health >> 4) + 1

    @property
    def _x_position(self):
        """Return the current horizontal position."""
        return self._read_mem(0x0014) * 0x100 + self._read_mem(0x0028)

    @property
    def _y_position(self):
        """Return the current vertical position."""
        return self._read_mem(0x001e) * 0x100 + self._read_mem(0x0032)

    @property
    def _level_transition(self):
        """Return the current level transition state."""
        return self._read_mem(0x04ec)

    @property
    def _is_dying(self):
        """Return True if the player is in a death transition."""
        return self._level_transition == _LEVEL_TRANSITION_RESTART

    @property
    def _is_dead(self):
        """Return True if the game is over."""
        return self._level_transition == _LEVEL_TRANSITION_GAME_OVER

    @property
    def _is_game_over(self):
        """Return True if the game has ended, False otherwise."""
        return self._is_dead or self._lives == 0

    @property
    def _is_level_complete(self):
        """Return True if the current level is complete or warped."""
        return self._level_transition in (
            _LEVEL_TRANSITION_COMPLETE,
            _LEVEL_TRANSITION_WARP,
        )

    # MARK: RAM Hacks

    def _write_stage(self):
        """Write the target level data before character selection."""
        self.ram[0x0531] = self._target_level
        self.ram[0x0635] = self._target_world - 1

    def _advance_until(self, predicate, max_frames):
        """Advance frames until predicate returns true."""
        for _ in range(max_frames):
            if predicate():
                return
            self._frame_advance(0)
        raise RuntimeError('timed out while starting Super Mario Bros. 2')

    def _skip_start_screen(self):
        """Skip title and character selection screens."""
        # wait for the title screen to initialize
        for _ in range(120):
            self._frame_advance(0)
        # press start to open character select
        while self._lives == 0:
            self._frame_advance(8)
            self._frame_advance(0)
        for _ in range(120):
            self._frame_advance(0)
        # stage environments patch the level before selecting Mario
        if self.is_single_stage_env:
            self._write_stage()
        # select Mario
        self._frame_advance(1)
        self._frame_advance(0)
        self._advance_until(
            lambda: self._health > 0 and self._x_position > 0,
            720,
        )
        # allow the entrance animation to reach a stable control point
        for _ in range(240):
            self._frame_advance(0)
        self._x_position_last = self._x_position

    # MARK: Reward Function

    @property
    def _x_reward(self):
        """Return the reward based on left right movement between steps."""
        _reward = self._x_position - self._x_position_last
        self._x_position_last = self._x_position
        if _reward < -5 or _reward > 5:
            return 0
        return _reward

    @property
    def _death_penalty(self):
        """Return the reward earned by dying."""
        if self._is_dying or self._is_dead:
            return -25
        return 0

    # MARK: nes-py API calls

    def _will_reset(self):
        """Handle and RAM hacking before a reset occurs."""
        self._x_position_last = 0

    def _did_reset(self):
        """Handle any RAM hacking after a reset occurs."""
        self._x_position_last = self._x_position

    def _get_reward(self):
        """Return the reward after a step occurs."""
        return self._x_reward + self._death_penalty

    def _get_terminated(self):
        """Return True if the episode is over, False otherwise."""
        if self.is_single_stage_env:
            return self._is_dying or self._is_dead or self._is_level_complete
        return self._is_game_over

    def _get_info(self):
        """Return the info after a step occurs."""
        return dict(
            character=self._character,
            cherries=self._cherries,
            coins=self._coins,
            health=self._health,
            level=self._level,
            level_complete=self._is_level_complete,
            life=self._life,
            stage=self._stage,
            world=self._world,
            x_pos=self._x_position,
            y_pos=self._y_position,
        )


# explicitly define the outward facing API of this module
__all__ = [
    SuperMarioBros2Env.__name__,
    _decode_smb2_level.__name__,
    _decode_smb2_target.__name__,
]
