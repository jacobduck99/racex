from dataclasses import dataclass

class CornerDetector:
    def __init__(self):
        self.car_rotating = False
        self.braking = False
        self.corners = []
        self.brake = []
        self.throttle = []

    def open_corner(self, pct, t):
        if not self.car_rotating:
            self.car_rotating = True
            self.rotating_pct = pct
            self.rotating_t = t

    def brake_on(self, pct, t, b):
        brake_on = 0.05 
        if not self.braking and b >= brake_on:
            self.braking = True
            self.brake_start_pct = pct
            self.brake_start_t = t

    def brake_off(self, pct, t, b):
        brake_off = 0.05
        if self.braking and b <= brake_off:
            self.braking = False
            self.brake_off_pct = pct
            self.brake_off_t = t

    def close_corner(self, pct, t):
        if self.car_rotating:
            self.car_rotating = False
            self.rotation_ended_pct = pct
            self.rotation_ended_t = t
            completed_corner = Corner(self.rotating_pct, self.rotating_t, self.rotation_ended_pct, self.rotation_ended_t)
            self.corners.append(completed_corner)

@dataclass
class Corner:
    rotating_pct: float
    rotating_t: float 
    rotation_ended_pct: float 
    rotation_ended_t: float        
    brake_started: float



