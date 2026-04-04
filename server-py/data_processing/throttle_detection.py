from dataclasses import dataclass
from typing import Optional

class ThrottleDetection:
    def __init__(self, throttle_on_threshold=0.1, throttle_off_threshold=0.2):
        self.throttle_on_threshold = throttle_on_threshold
        self.throttle_off_threshold = throttle_off_threshold
        self.throttle_on_t = None
        self.throttle_on_pct = None
        self.throttle_off_t = None
        self.throttle_off_pct = None
        self.last_gear = None
        self.throttle_inputs = []
        self.gear = None

    def throttle_off(self, pct, t, throttle):
        if throttle <= self.throttle_off_threshold:
            self.throttle_off_t = t
            self.throttle_off_pct = pct

    def throttle_on(self, pct, t, throttle, gear):
        if self.throttle_off_pct is not None:
            if throttle >= self.throttle_on_threshold:
                self.throttle_on_pct = pct
                self.throttle_on_t = t
                if gear != 0:
                    self.last_gear = gear
                apex = Throttle(self.throttle_off_pct, self.throttle_off_t,self.throttle_on_pct, self.throttle_on_t, self.last_gear) 
                self.throttle_inputs.append(apex)
                self.throttle_off_pct = None

@dataclass
class Throttle:
    throttle_off_pct: float
    throttle_off_t: float
    throttle_on_pct: float
    throttle_on_t: float
    gear: int
