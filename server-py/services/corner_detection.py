from dataclasses import dataclass
from typing import Optional

class CornerDetector:
    def __init__(self, brake_on_threshold=0.05, brake_off_threshold=0.05, throttle_on_threshold=0.1, throttle_off_threshold=0.2):
        self.car_rotating = False
        self.braking = False
        self.corners = []
        self.brake_zones = []
        self.brake_on_threshold = brake_on_threshold
        self.brake_on_pct = None
        self.brake_off_threshold = brake_off_threshold
        self.throttle_on_threshold = throttle_on_threshold
        self.throttle_off_threshold = throttle_off_threshold
        self.throttle_on_t = None
        self.throttle_on_pct = None
        self.throttle_off_t = None
        self.throttle_off_pct = None
        self.throttle = []

    def open_corner(self, pct, t):
        if not self.car_rotating:
            self.car_rotating = True
            self.rotating_pct = pct
            self.rotating_t = t

    def throttle_off(self, pct, t, throttle):
        if self.throttle_on_pct is not None and throttle <= self.throttle_off_threshold:
            self.throttle_off_t = t
            self.throttle_off_pct = pct
            
    def brake_on(self, pct, t, b):
        if not self.braking and b >= self.brake_on_threshold:
            self.braking = True
            self.brake_on_pct = pct
            self.brake_on_t = t

    def brake_off(self, pct, t, b):
        if self.braking and b <= self.brake_off_threshold:
            self.braking = False
            self.brake_off_pct = pct
            self.brake_off_t = t
            completed_braking_zones = Brake(self.brake_on_pct, self.brake_on_t,self.brake_off_pct, self.brake_off_t)
            self.brake_zones.append(completed_braking_zones)

    def throttle_on(self, pct, t, throttle):
        if not self.braking:
            if throttle >= self.throttle_on_threshold and self.throttle_off_pct is not None:
                self.throttle_on_t = t
                self.throttle_on_pct = pct
                apex = Throttle(self.throttle_off_pct, self.throttle_off_t, self.throttle_on_pct, self.throttle_on_t) 
                self.throttle.append(apex)
                self.throttle_off_pct = None

    def close_corner(self, pct, t):
        if self.car_rotating:
            self.car_rotating = False
            self.rotation_ended_pct = pct
            self.rotation_ended_t = t
            if self.brake_on_pct is not None:
                completed_corner = Corner(self.rotating_pct, self.rotating_t, self.rotation_ended_pct, self.rotation_ended_t)
            self.corners.append(completed_corner)

@dataclass
class Brake:
    brake_on_pct: float  
    brake_on_t: float 
    brake_off_pct: float 
    brake_off_t: float

@dataclass
class Throttle:
    throttle_on_pct: float
    throttle_on_t: float
    throttle_off_pct: float
    throttle_off_t: float

@dataclass
class Corner:
    rotating_pct: float
    rotating_t: float 
    rotation_ended_pct: float 
    rotation_ended_t: float
    brake_zone: Optional[Brake] = None
    brake_on_pct: Optional[float] = None    
    brake_on_t: Optional[float] = None
    brake_off_pct: Optional[float] = None
    brake_off_t: Optional[float] = None
    throttle: Optional[Throttle] = None


