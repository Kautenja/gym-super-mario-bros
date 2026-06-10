"""A Gymnasium environment for Super Mario Bros. 2 (USA)."""
from nes_py import NESEnv
from ._roms import smb2_rom_path
from .tasks import task_for_config


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
        self._rom_mode = 'vanilla'
        self._rom_version = 0
        target = _decode_smb2_target(target)
        self._target_world, self._target_stage, self._target_level = target
        self._position_origin = (0, 0)
        self._position_progress_max = 0
        self._coins_last = 0
        self._cherries_last = 0
        self._health_last = 0
        self._completion_rewarded = False
        self._last_reward_components = {}
        self._last_reward_unclipped = 0.0
        self._last_reward_clipped = 0.0
        self.reset()
        self._skip_start_screen()
        self._backup()

    @property
    def is_single_stage_env(self):
        """Return True if this environment is a stage environment."""
        return self._target_level is not None

    @property
    def _task(self):
        """Return metadata for the current configured task."""
        world = None
        stage = None
        if self.is_single_stage_env:
            world = self._target_world
            stage = self._target_stage
        return task_for_config(
            'smb2_usa',
            self._rom_version,
            world=world,
            stage=stage,
        )

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
    def _health_meter(self):
        """Return the raw life meter bar count."""
        return self._read_mem(0x04c3)

    @property
    def _character_status(self):
        """Return the raw character status byte."""
        return self._read_mem(0x00c7)

    @property
    def _invulnerability_timer(self):
        """Return the invulnerability timer."""
        return self._read_mem(0x0085)

    @property
    def _enemy_defeat_count(self):
        """Return the enemies defeated toward the next heart drop."""
        return self._read_mem(0x04ad)

    @property
    def _item_in_hand_height(self):
        """Return the raw item-in-hand height byte."""
        return self._read_mem(0x00ae)

    @property
    def _subspace_visits(self):
        """Return the current subspace coin-grab attempt counter."""
        return self._read_mem(0x0621)

    @property
    def _x_position(self):
        """Return the current horizontal position."""
        return self._read_mem(0x0014) * 0x100 + self._read_mem(0x0028)

    @property
    def _x_page(self):
        """Return the current horizontal page."""
        return self._read_mem(0x0014)

    @property
    def _x_screen(self):
        """Return the current horizontal screen position."""
        return self._read_mem(0x0028)

    @property
    def _y_position(self):
        """Return the current vertical position."""
        return self._read_mem(0x001e) * 0x100 + self._read_mem(0x0032)

    @property
    def _y_page(self):
        """Return the current vertical page."""
        return self._read_mem(0x001e)

    @property
    def _y_screen(self):
        """Return the current vertical screen position."""
        return self._read_mem(0x0032)

    @property
    def _position_progress(self):
        """Return Manhattan distance from the reset start position."""
        x_origin, y_origin = self._position_origin
        return abs(self._x_position - x_origin) + abs(self._y_position - y_origin)

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
        self._position_origin = (self._x_position, self._y_position)
        self._position_progress_max = 0
        self._coins_last = self._coins
        self._cherries_last = self._cherries
        self._health_last = self._health
        self._completion_rewarded = False

    # MARK: Reward Function

    @property
    def _progress_reward(self):
        """Return the reward for reaching a new best distance from start."""
        _reward = self._position_progress - self._position_progress_max
        if _reward <= 0:
            return 0
        self._position_progress_max = self._position_progress
        if _reward > 10:
            return 0
        return _reward

    @property
    def _death_penalty(self):
        """Return the reward earned by dying."""
        if self._is_dying or self._is_dead:
            return -25
        return 0

    @property
    def _collectible_reward(self):
        """Return the reward for SMB2 collectible counters."""
        coins_reward = self._coins - self._coins_last
        cherries_reward = self._cherries - self._cherries_last
        self._coins_last = self._coins
        self._cherries_last = self._cherries
        if coins_reward < 0:
            coins_reward = 0
        if cherries_reward < 0:
            cherries_reward = 0
        return coins_reward * 5 + cherries_reward * 2

    @property
    def _health_reward(self):
        """Return the reward for gaining or losing health."""
        _reward = self._health - self._health_last
        self._health_last = self._health
        return _reward * 5

    @property
    def _completion_reward(self):
        """Return the reward for completing or warping from a level."""
        if self._is_level_complete and not self._completion_rewarded:
            self._completion_rewarded = True
            return 50
        return 0

    def _clip_reward_value(self, reward):
        """Return reward clamped to the public reward range."""
        return max(self.reward_range[0], min(self.reward_range[1], reward))

    def _store_reward_components(self, components):
        """Store the last per-step reward diagnostics."""
        self._last_reward_components = {
            key: float(value)
            for key, value in components.items()
        }
        self._last_reward_unclipped = float(sum(self._last_reward_components.values()))
        self._last_reward_clipped = float(
            self._clip_reward_value(self._last_reward_unclipped)
        )

    def _reset_reward_components(self):
        """Reset per-step reward diagnostics."""
        self._last_reward_components = dict(
            progress=0.0,
            collectibles=0.0,
            health=0.0,
            completion=0.0,
            death=0.0,
        )
        self._last_reward_unclipped = 0.0
        self._last_reward_clipped = 0.0

    def _reward_info(self):
        """Return reward diagnostics for the info dictionary."""
        return dict(
            reward_components=dict(self._last_reward_components),
            reward_total_unclipped=self._last_reward_unclipped,
            reward_total_clipped=self._last_reward_clipped,
        )

    def _normalized_info(self):
        """Return cross-game metrics for training and evaluation code."""
        task = self._task
        death = self._is_dying or self._is_dead
        return dict(
            clear=self._is_level_complete,
            death=death,
            game=task.game,
            game_family=task.game_family,
            progress=self._position_progress,
            progress_max=self._position_progress_max,
            rom_mode=self._rom_mode,
            single_stage=self.is_single_stage_env,
            task_id=task.task_id,
            target_stage=self._target_stage,
            target_world=self._target_world,
            timeout=False,
            world_label=str(self._world),
        )

    # MARK: nes-py API calls

    def _will_reset(self):
        """Handle and RAM hacking before a reset occurs."""
        self._position_origin = (0, 0)
        self._position_progress_max = 0
        self._coins_last = 0
        self._cherries_last = 0
        self._health_last = 0
        self._completion_rewarded = False
        self._reset_reward_components()

    def _did_reset(self):
        """Handle any RAM hacking after a reset occurs."""
        self._position_origin = (self._x_position, self._y_position)
        self._position_progress_max = 0
        self._coins_last = self._coins
        self._cherries_last = self._cherries
        self._health_last = self._health
        self._completion_rewarded = False
        self._reset_reward_components()

    def _get_reward(self):
        """Return the reward after a step occurs."""
        self._store_reward_components(
            dict(
                progress=self._progress_reward,
                collectibles=self._collectible_reward,
                health=self._health_reward,
                completion=self._completion_reward,
                death=self._death_penalty,
            )
        )
        return self._last_reward_unclipped

    def _get_terminated(self):
        """Return True if the episode is over, False otherwise."""
        if self.is_single_stage_env:
            return self._is_dying or self._is_dead or self._is_level_complete
        return self._is_game_over

    def _get_info(self):
        """Return the info after a step occurs."""
        info = dict(
            character=self._character,
            character_id=self._read_mem(0x008f),
            character_status=self._character_status,
            cherries=self._cherries,
            coins=self._coins,
            enemy_defeat_count=self._enemy_defeat_count,
            health_meter=self._health_meter,
            health=self._health,
            invulnerability_timer=self._invulnerability_timer,
            is_dead=self._is_dead,
            is_dying=self._is_dying,
            is_game_over=self._is_game_over,
            item_in_hand_height=self._item_in_hand_height,
            level=self._level,
            level_complete=self._is_level_complete,
            level_transition=self._level_transition,
            life=self._life,
            lives=self._lives,
            position_progress=self._position_progress,
            position_progress_max=self._position_progress_max,
            stage=self._stage,
            subspace_visits=self._subspace_visits,
            world=self._world,
            x_page=self._x_page,
            x_pos=self._x_position,
            x_screen=self._x_screen,
            y_page=self._y_page,
            y_pos=self._y_position,
            y_screen=self._y_screen,
        )
        info.update(self._normalized_info())
        info.update(self._reward_info())
        return info


# explicitly define the outward facing API of this module
__all__ = [
    SuperMarioBros2Env.__name__,
    _decode_smb2_level.__name__,
    _decode_smb2_target.__name__,
]
