"""A Gymnasium environment for Super Mario Bros. 3."""
from collections import defaultdict

from nes_py import NESEnv

from ._roms import smb3_rom_path
from .smb3_stages import SMB3_VALIDATED_STAGES
from .tasks import task_for_config


_STATUS_MAP = defaultdict(
    lambda: 'unknown',
    {
        0x00: 'small',
        0x01: 'super',
        0x02: 'fire',
        0x03: 'raccoon',
        0x04: 'frog',
        0x05: 'tanooki',
        0x06: 'hammer',
    },
)

_MAP_START = (0x40, 0x20)
_WORLD_1_LEVEL_1_PANEL = (0x20, 0x40)
_WORLD_1_LEVEL_1_JUNCTION = (0x40, 0x40)
_MAP_PLAYER_Y = 0x0075
_MAP_PLAYER_X_HI = 0x0077
_MAP_PLAYER_X = 0x0079
_MAP_PLAYER_MOVE = 0x007b
_MAP_PLAYER_DIRECTION = 0x007d
_MAP_PLAYER_TILE = 0x00e5


_SMB3_STAGE_ENTRY_RECIPES = {
    (1, 1): dict(
        start=(0x40, 0x40, 0x00, 0x4a, 0x01),
        action=16,
        panel=_WORLD_1_LEVEL_1_PANEL,
    ),
    (1, 2): dict(
        start=(0x20, 0x60, 0x00, 0x47, 0x01),
        action=128,
        panel=(0x20, 0x80),
    ),
    (1, 4): dict(
        start=(0x40, 0x80, 0x00, 0x46, 0x04),
        action=128,
        panel=(0x40, 0xa0),
    ),
    (1, 6): dict(
        start=(0xa0, 0x60, 0x00, 0xa3, 0x01),
        action=128,
        panel=(0xa0, 0x80),
    ),
}


def _decode_smb3_target(target):
    """
    Return the target world and stage.

    Args:
        target (None, tuple): the optional (world, stage) target

    Returns:
        a tuple of (world, stage)

    """
    if target is None:
        return None, None
    if not isinstance(target, tuple):
        raise TypeError('target must be of type tuple')

    target_world, target_stage = target
    if not isinstance(target_world, int):
        raise TypeError('target_world must be of type: int')
    if not isinstance(target_stage, int):
        raise TypeError('target_stage must be of type: int')
    if (target_world, target_stage) not in SMB3_VALIDATED_STAGES:
        raise ValueError(
            'target must be one of: {}'.format(
                ', '.join('{}-{}'.format(*target) for target in SMB3_VALIDATED_STAGES)
            )
        )

    return target_world, target_stage


class SuperMarioBros3Env(NESEnv):
    """An environment for playing Super Mario Bros. 3."""

    # the legal range of rewards for each step
    reward_range = (-15, 15)

    def __init__(self, target=None, render_mode=None):
        """
        Initialize a new Super Mario Bros. 3 environment.

        Args:
            target (tuple): a tuple of the (world, stage) to play as a level
            render_mode (str): the render mode to use, if any

        Returns:
            None

        """
        rom = smb3_rom_path()
        super(SuperMarioBros3Env, self).__init__(rom, render_mode=render_mode)
        self._rom_mode = 'vanilla'
        self._rom_version = 0
        self._target_world, self._target_stage = _decode_smb3_target(target)
        self._current_world = 1
        self._current_stage = 1
        self._entered_level = False
        self._life_start = 0
        self._life_last = 0
        self._time_last = 0
        self._x_position_max = 0
        self._score_last = 0
        self._status_last = 0
        self._completion_rewarded = False
        self._life_loss_pending = False
        self._last_reward_components = {}
        self._last_reward_unclipped = 0.0
        self._last_reward_clipped = 0.0
        self.reset()
        self._skip_start_screen()
        self._backup()

    @property
    def is_single_stage_env(self):
        """Return True if this environment is a stage environment."""
        return self._target_world is not None

    @property
    def _task(self):
        """Return metadata for the current configured task."""
        world = None
        stage = None
        if self.is_single_stage_env:
            world = self._target_world
            stage = self._target_stage
        return task_for_config(
            'smb3',
            self._rom_version,
            world=world,
            stage=stage,
        )

    # MARK: Memory access

    def _read_mem(self, address):
        """Read one RAM byte as a Python integer."""
        return int(self.ram[address])

    def _read_mem_range(self, address, length):
        """
        Read a range of bytes where each byte is a 10's place figure.

        Args:
            address (int): the address to read from as a 16 bit integer
            length: the number of sequential bytes to read

        Returns:
            the integer value of this 10's place representation

        """
        return int(''.join(map(str, map(int, self.ram[address:address + length]))))

    def _read_big_endian(self, address, length):
        """
        Read a big-endian integer from RAM.

        Args:
            address (int): the address to read from as a 16 bit integer
            length: the number of sequential bytes to read

        Returns:
            the integer value of the memory range

        """
        value = 0
        for byte in self.ram[address:address + length]:
            value = (value << 8) + int(byte)
        return value

    @property
    def _world(self):
        """Return the current world (1 to 8)."""
        if self._read_mem(0x0727) < 8:
            return self._read_mem(0x0727) + 1
        return self._current_world

    @property
    def _stage(self):
        """Return the current stage within the world."""
        return self._current_stage

    @property
    def _score(self):
        """Return the current player score."""
        return self._read_big_endian(0x0715, 3) * 10

    @property
    def _time(self):
        """Return the time left."""
        return self._read_mem_range(0x05ee, 3)

    @property
    def _life(self):
        """Return the number of remaining lives."""
        return self._read_mem(0x0736)

    @property
    def _p_meter(self):
        """Return the current P-meter status byte."""
        return self._read_mem(0x03dd)

    @property
    def _p_meter_full(self):
        """Return True if the P-meter's P indicator is active."""
        return bool(self._p_meter & 0x40)

    @property
    def _pipe_timer(self):
        """Return the pipe transition countdown timer."""
        return self._read_mem(0x0510)

    @property
    def _p_meter_timer(self):
        """Return the P-meter update countdown timer."""
        return self._read_mem(0x0515)

    @property
    def _invulnerability_timer(self):
        """Return the player hit invulnerability timer."""
        return self._read_mem(0x0552)

    @property
    def _star_timer(self):
        """Return the star power timer."""
        return self._read_mem(0x0553)

    @property
    def _flight_timer(self):
        """Return the raccoon flight timer."""
        return self._read_mem(0x056e)

    @property
    def _card_selection(self):
        """Return the current flashing end-card selection."""
        return self._read_mem(0x066f)

    @property
    def _map_y(self):
        """Return the current map y position."""
        return self._read_mem(0x0075)

    @property
    def _map_x(self):
        """Return the current map x position."""
        return self._read_mem(0x0079)

    @property
    def _map_position(self):
        """Return the current map position as a (y, x) tuple."""
        return self._map_y, self._map_x

    @property
    def _is_on_map(self):
        """Return True if the player is currently on the world map."""
        return self._time == 0 and any(self._map_position)

    @property
    def _is_in_level(self):
        """Return True if the player is currently in a level."""
        return self._time > 0

    @property
    def _x_position(self):
        """Return the current horizontal position."""
        if self._is_in_level:
            return self._x_page * 0x100 + self._x_screen
        return self._map_x

    @property
    def _y_position(self):
        """Return the current vertical position."""
        if self._is_in_level:
            return self._y_page * 0x100 + self._y_screen
        return self._map_y

    @property
    def _x_page(self):
        """Return the current horizontal page."""
        return self._read_mem(0x0075)

    @property
    def _x_screen(self):
        """Return the current horizontal screen position."""
        return self._read_mem(0x0090)

    @property
    def _y_page(self):
        """Return the current vertical page."""
        return self._read_mem(0x0087)

    @property
    def _y_screen(self):
        """Return the current vertical screen position."""
        return self._read_mem(0x00a2)

    @property
    def _player_status(self):
        """Return the player status as a string."""
        return _STATUS_MAP[self._status_value]

    @property
    def _status_value(self):
        """Return the raw player status value."""
        return self._read_mem(0x00ed)

    @property
    def _powerup_level(self):
        """Return a compact powerup level for reward shaping."""
        return min(self._status_value, 2)

    @property
    def _is_dying(self):
        """Return True if the player has lost a life this attempt."""
        return self._life != 0xff and self._life < self._life_start

    @property
    def _is_game_over(self):
        """Return True if the game has ended, False otherwise."""
        return self._life == 0xff

    @property
    def _flag_get(self):
        """Return True if a single-stage attempt returned to the map alive."""
        return (
            self._entered_level and
            self._is_on_map and
            not self._is_dying and
            not self._life_loss_pending and
            not self._is_game_over
        )

    # MARK: RAM Hacks

    def _advance_until(self, predicate, max_frames):
        """Advance frames until predicate returns true."""
        for _ in range(max_frames):
            if predicate():
                return
            self._frame_advance(0)
        raise RuntimeError('timed out while starting Super Mario Bros. 3')

    def _press_and_release(self, action):
        """Press and release a controller action."""
        self._frame_advance(action)
        self._frame_advance(0)

    def _walk_map(self, action, target):
        """Walk on the world map until the target coordinate is reached."""
        for _ in range(12):
            if self._map_position == target:
                return
            self._press_and_release(action)
            for _ in range(30):
                self._frame_advance(0)
        raise RuntimeError('timed out while walking Super Mario Bros. 3 map')

    def _enter_world_1_level_1(self):
        """Enter World 1-1 from the World 1 map start."""
        self._walk_map(128, _WORLD_1_LEVEL_1_JUNCTION)
        self._walk_map(16, _WORLD_1_LEVEL_1_PANEL)
        self._enter_map_panel()
        self._current_world = 1
        self._current_stage = 1

    def _write_map_entry_start(self, recipe):
        """Place Mario on a map path next to the target panel."""
        y, x, x_hi, tile, direction = recipe['start']
        self.ram[_MAP_PLAYER_Y] = y
        self.ram[_MAP_PLAYER_X_HI] = x_hi
        self.ram[_MAP_PLAYER_X] = x
        self.ram[_MAP_PLAYER_MOVE] = 0
        self.ram[_MAP_PLAYER_DIRECTION] = direction
        self.ram[_MAP_PLAYER_TILE] = tile

    def _enter_map_panel(self):
        """Enter the currently selected world-map panel."""
        for _ in range(120):
            self._frame_advance(0)
        self._press_and_release(1)
        self._advance_until(
            lambda: self._is_in_level and self._x_position > 0,
            720,
        )
        for _ in range(180):
            self._frame_advance(0)
        self._entered_level = True

    def _enter_target_stage(self):
        """Enter the configured validated SMB3 stage from the World 1 map."""
        target = (self._target_world, self._target_stage)
        recipe = _SMB3_STAGE_ENTRY_RECIPES[target]
        self._write_map_entry_start(recipe)
        for _ in range(10):
            self._frame_advance(0)
        self._walk_map(recipe['action'], recipe['panel'])
        self._enter_map_panel()
        self._current_world = self._target_world
        self._current_stage = self._target_stage

    def _skip_start_screen(self):
        """Skip title and map screens to reach the first playable level."""
        for _ in range(300):
            self._frame_advance(0)
        self._advance_until_map_start()
        for _ in range(120):
            self._frame_advance(0)
        if self.is_single_stage_env:
            self._enter_target_stage()
        else:
            self._enter_world_1_level_1()
        self._life_start = self._life
        self._life_last = self._life
        self._time_last = self._time
        self._x_position_max = self._x_position
        self._score_last = self._score
        self._status_last = self._powerup_level
        self._completion_rewarded = False

    def _advance_until_map_start(self):
        """Press start until the World 1 map start is active."""
        for _ in range(300):
            if self._map_position == _MAP_START:
                return
            self._press_and_release(8)
            for _ in range(10):
                self._frame_advance(0)
        raise RuntimeError('timed out while opening Super Mario Bros. 3 map')

    # MARK: Reward Function

    @property
    def _progress_reward(self):
        """Return the reward for reaching a new best horizontal position."""
        if not self._is_in_level:
            self._x_position_max = self._x_position
            return 0
        _reward = self._x_position - self._x_position_max
        if _reward <= 0:
            return 0
        self._x_position_max = self._x_position
        if _reward > 5:
            return 0
        return _reward

    @property
    def _time_penalty(self):
        """Return the reward for the in-game clock ticking."""
        if not self._is_in_level:
            self._time_last = self._time
            return 0
        _reward = self._time - self._time_last
        self._time_last = self._time
        if _reward > 0:
            return 0
        return _reward

    @property
    def _death_penalty(self):
        """Return the reward earned by losing a life."""
        if self._life != 0xff and self._life < self._life_last:
            self._life_last = self._life
            return -25
        self._life_last = self._life
        return 0

    @property
    def _score_reward(self):
        """Return the reward for increasing the in-game score."""
        _reward = self._score - self._score_last
        self._score_last = self._score
        if _reward <= 0:
            return 0
        return _reward / 100

    @property
    def _powerup_reward(self):
        """Return the reward for powerup gains and losses."""
        _reward = self._powerup_level - self._status_last
        self._status_last = self._powerup_level
        return _reward * 5

    @property
    def _completion_reward(self):
        """Return the reward for completing a stage."""
        if self._flag_get and not self._completion_rewarded:
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
            time=0.0,
            score=0.0,
            powerup=0.0,
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
        death = self._is_dying or self._is_game_over
        return dict(
            clear=self._flag_get,
            death=death,
            game=task.game,
            game_family=task.game_family,
            progress=self._x_position,
            progress_max=self._x_position_max,
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
        """Handle RAM bookkeeping before a reset occurs."""
        self._entered_level = False
        self._life_start = 0
        self._life_last = 0
        self._time_last = 0
        self._x_position_max = 0
        self._score_last = 0
        self._status_last = 0
        self._completion_rewarded = False
        self._life_loss_pending = False
        self._reset_reward_components()

    def _did_reset(self):
        """Handle RAM bookkeeping after a reset occurs."""
        self._entered_level = self._is_in_level
        self._life_start = self._life
        self._life_last = self._life
        self._time_last = self._time
        self._x_position_max = self._x_position
        self._score_last = self._score
        self._status_last = self._powerup_level
        self._completion_rewarded = False
        self._life_loss_pending = False
        self._reset_reward_components()

    def _did_step(self, done):
        """Handle non-terminal map returns after a life loss."""
        if done:
            return
        if self._is_in_level:
            self._life_loss_pending = False
            return
        if self._is_dying and not self._is_game_over:
            self._life_loss_pending = True
            self._life_start = self._life
            self._life_last = self._life
            self._time_last = self._time
            self._x_position_max = self._x_position

    def _get_reward(self):
        """Return the reward after a step occurs."""
        self._store_reward_components(
            dict(
                progress=self._progress_reward,
                time=self._time_penalty,
                score=self._score_reward,
                powerup=self._powerup_reward,
                completion=self._completion_reward,
                death=self._death_penalty,
            )
        )
        return self._last_reward_unclipped

    def _get_terminated(self):
        """Return True if the episode is over, False otherwise."""
        if self.is_single_stage_env:
            return self._is_dying or self._flag_get or self._is_game_over
        return self._is_game_over

    def _get_info(self):
        """Return the info after a step occurs."""
        info = dict(
            card_selection=self._card_selection,
            flag_get=self._flag_get,
            flight_timer=self._flight_timer,
            in_level=self._is_in_level,
            invulnerability_timer=self._invulnerability_timer,
            is_dying=self._is_dying,
            is_game_over=self._is_game_over,
            life=self._life,
            lives=self._life,
            map_x=self._map_x,
            map_y=self._map_y,
            p_meter=self._p_meter,
            p_meter_full=self._p_meter_full,
            p_meter_timer=self._p_meter_timer,
            pipe_timer=self._pipe_timer,
            powerup_level=self._powerup_level,
            score=self._score,
            stage=self._stage,
            star_timer=self._star_timer,
            status=self._player_status,
            status_value=self._status_value,
            time=self._time,
            world=self._world,
            x_page=self._x_page,
            x_pos=self._x_position,
            x_pos_max=self._x_position_max,
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
    SuperMarioBros3Env.__name__,
    _decode_smb3_target.__name__,
]
