"""Wrappers for altering the functionality of the game."""
from .clip_reward_env import ClipRewardEnv
from .downsample_env import DownsampleEnv
from .frame_stack_env import FrameStackEnv
from .max_frameskip_env import MaxFrameskipEnv
from .monitor import Monitor
from .penalize_death_env import PenalizeDeathEnv
from .reward_cache_env import RewardCacheEnv


# explicitly define the outward facing API of this package
__all__ = [
    ClipRewardEnv.__name__,
    DownsampleEnv.__name__,
    FrameStackEnv.__name__,
    MaxFrameskipEnv.__name__,
    Monitor.__name__,
    PenalizeDeathEnv.__name__,
    RewardCacheEnv.__name__,
]
