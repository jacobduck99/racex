from dataclasses import dataclass
from typing import Optional

from data_processing.brake_detection import Brake
from data_processing.throttle_detection import Throttle 

@dataclass
class Corner:
    rotating_pct: float
    rotating_t: float 
    rotation_ended_pct: float 
    rotation_ended_t: float
    brake_zone: Optional[Brake] = None
    min_speed: Optional[float] = None
    throttle: Optional[Throttle] = None
    yaw_rate: Optional[float] = None
    gear: Optional[int] = None

@dataclass
class Matched:
    fast: list
    ref: list
    fast_corner_time: list
    ref_corner_time: list
    delta: float
    corner_num: int = None
