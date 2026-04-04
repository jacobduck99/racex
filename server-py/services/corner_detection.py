from dataclasses import dataclass
from typing import Optional
from services.utils import convert_to_kph
from data_processing.brake_detection import Brake

class CornerDetector:
    def __init__(self, throttle_on_threshold=0.1, throttle_off_threshold=0.2):
        self.car_rotating = False
        self.corners = []
        self.throttle_on_threshold = throttle_on_threshold
        self.throttle_off_threshold = throttle_off_threshold
        self.throttle_on_t = None
        self.throttle_on_pct = None
        self.throttle_off_t = None
        self.throttle_off_pct = None
        self.last_full_throttle_pcts = []
        self.gear = None
        self.current_min_speed = float('inf')
        self.min_speed_pct = None
        self.min_speed_kph = None
        self.throttle = []
        self.rotating_pct = None
        self.previous_corner = None
        self.merged_corners = []

    def open_corner(self, pct, t, yaw_rate):
        if not self.car_rotating:
            self.car_rotating = True
            self.rotating_pct = pct
            self.rotating_t = t
            self.yaw_rate = yaw_rate

    def throttle_off(self, pct, t, throttle):
        if throttle <= self.throttle_off_threshold:
            self.throttle_off_t = t
            self.throttle_off_pct = pct
            
    def min_speed(self, spd, pct):
        if self.car_rotating and self.rotating_pct is not None:
            if spd < self.current_min_speed:
                self.current_min_speed = spd 
                self.min_speed_pct = pct
                self.min_speed_kph = convert_to_kph(self.current_min_speed)

    def throttle_on(self, pct, t, throttle, gear):
        if not self.braking and self.throttle_off_pct is not None:
            if throttle >= self.throttle_on_threshold:
                self.throttle_on_pct = pct
                self.throttle_on_t = t
                self.gear = gear
                apex = Throttle(self.throttle_off_pct, self.throttle_off_t,self.throttle_on_pct, self.throttle_on_t, self.gear) 
                self.throttle.append(apex)
                self.throttle_off_pct = None

    def close_corner(self, pct, t, min_speed, yaw_rate):
        if self.car_rotating:
            self.car_rotating = False
            self.rotation_ended_pct = pct
            self.rotation_ended_t = t
            self.yaw_rate = yaw_rate
            completed_corner = Corner(self.rotating_pct, self.rotating_t, self.rotation_ended_pct, self.rotation_ended_t, min_speed=self.min_speed_kph, yaw_rate=self.yaw_rate)
            self.corners.append(completed_corner) 
            self.current_min_speed = float('inf')
            self.yaw_rate = None
            self.min_speed_kph = None

    def filter_corners(self, corners):
        clean_corners = []
        for corner in corners:
            corner_duration_pct = corner.rotation_ended_pct - corner.rotating_pct
            if corner_duration_pct > 0.004:  
                clean_corners.append(corner)
        return clean_corners

    def merge_corner(self, corners):
        for current_corner in corners:
            if self.previous_corner is None:
                self.previous_corner = current_corner
            else:
                gap_start = self.previous_corner.rotation_ended_pct
                gap_end = current_corner.rotating_pct
                gap = gap_end - gap_start

                if self.previous_corner.yaw_rate * current_corner.yaw_rate < 0:
                    self.merged_corners.append(self.previous_corner)
                    self.previous_corner = current_corner
                elif gap < 0.05:
                    self.previous_corner.rotation_ended_t = current_corner.rotation_ended_t
                    self.previous_corner.rotation_ended_pct = current_corner.rotation_ended_pct
                else:
                    self.merged_corners.append(self.previous_corner)
                    self.previous_corner = current_corner
        self.merged_corners.append(self.previous_corner)
        return self.merged_corners

@dataclass
class Throttle:
    throttle_off_pct: float
    throttle_off_t: float
    throttle_on_pct: float
    throttle_on_t: float
    gear: int

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

@dataclass
class Matched:
    fast: list
    ref: list
    corner_num: int = None



