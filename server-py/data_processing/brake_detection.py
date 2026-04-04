from dataclasses import dataclass
from typing import Optional

class BrakeDetector:
    def __init__(self, brake_on_threshold=0.05, brake_off_threshold=0.05):
        self.braking = False
        self.brake_zones = []
        self.brake_on_threshold = brake_on_threshold
        self.brake_on_pct = None
        self.max_brake_pressure = float('-inf')
        self.brake_off_threshold = brake_off_threshold

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




@dataclass
class Brake:
    brake_on_pct: float  
    brake_on_t: float 
    brake_off_pct: float 
    brake_off_t: float
    max_brake_pressure: float
