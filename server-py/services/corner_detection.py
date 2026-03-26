from dataclasses import dataclass
from typing import Optional
from services.utils import convert_to_kph1

class CornerDetector:
    def __init__(self, brake_on_threshold=0.05, brake_off_threshold=0.05, throttle_on_threshold=0.1, throttle_off_threshold=0.2):
        self.car_rotating = False
        self.braking = False
        self.corners = []
        self.brake_zones = []
        self.brake_on_threshold = brake_on_threshold
        self.brake_on_pct = None
        self.max_brake_pressure = float('-inf')
        self.brake_off_threshold = brake_off_threshold
        self.throttle_on_threshold = throttle_on_threshold
        self.throttle_off_threshold = throttle_off_threshold
        self.throttle_on_t = None
        self.throttle_on_pct = None
        self.throttle_off_t = None
        self.throttle_off_pct = None
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
            
    def brake_on(self, pct, t, b):
        if not self.braking and b >= self.brake_on_threshold:
            self.braking = True
            self.brake_on_pct = pct
            self.brake_on_t = t
            self.brake_pressure = b

    def max_brake(self, b):
        if self.braking:
            if b > self.max_brake_pressure:
                self.max_brake_pressure = b

    def brake_off(self, pct, t, b):
        if self.braking and b <= self.brake_off_threshold:
            self.braking = False
            self.brake_off_pct = pct
            self.brake_off_t = t
            completed_braking_zones = Brake(self.brake_on_pct, self.brake_on_t,self.brake_off_pct, self.brake_off_t, self.max_brake_pressure)
            self.brake_zones.append(completed_braking_zones)

    def min_speed(self, spd, pct):
        if self.car_rotating and self.rotating_pct is not None:
            if spd < self.current_min_speed:
                self.current_min_speed = spd 
                self.min_speed_pct = pct
                self.min_speed_kph = convert_to_kph1(self.current_min_speed)

    def throttle_on(self, pct, t, throttle, gear):
        if not self.braking and self.throttle_off_pct is not None:
            if throttle >= self.throttle_on_threshold:
                self.throttle_on_pct = pct
                self.throttle_on_t = t
                self.gear = gear
                apex = Throttle(self.throttle_on_pct, self.throttle_on_t, self.throttle_off_pct, self.throttle_off_t, self.gear) 
                self.throttle.append(apex)
                print("throttle", self.throttle)
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

    def merge_corner(self, corners):
        for next_corner in corners:
            if self.previous_corner is None:
                self.previous_corner = next_corner
            else:
                time_to_next_corner = self.previous_corner.rotation_ended_t - next_corner.rotating_t

                if time_to_next_corner < 0.5 and self.previous_corner.yaw_rate * next_corner.yaw_rate > 0:
                    self.previous_corner.rotation_ended_t = next_corner.rotation_ended_t
                else:
                    self.merged_corners.append(self.previous_corner)
                    self.previous_corner = next_corner
        self.merged_corners.append(self.previous_corner)
        for i, c in enumerate(self.merged_corners, start=1):
            c.corner_num = i
        return self.merged_corners

@dataclass
class Brake:
    brake_on_pct: float  
    brake_on_t: float 
    brake_off_pct: float 
    brake_off_t: float
    max_brake_pressure: float

@dataclass
class Throttle:
    throttle_on_pct: float
    throttle_on_t: float
    throttle_off_pct: float
    throttle_off_t: float
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
    corner_num: Optional[int] = None


