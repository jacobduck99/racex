
class CornerDetector:
    def __init__(self):
        self.car_rotating = False
        self.corner = []

    def open_corner(self, pct, t):
        if not self.car_rotating:
            self.car_rotating = True
            self.rotating_pct = pct
            self.rotating_t = t

    def close_corner(self, pct, t):
        if self.car_rotating:
            self.car_rotating = False
            self.rotation_ended_pct = pct
            self.rotation_ended_t = t
            completed_corner = Corner(self.rotating_pct, self.rotating_t, self.rotation_ended_pct, self.rotation_ended_t)
            self.corner.append(completed_corner)

class Corner:
    def __init__(self, rotating_pct, rotating_t, rotation_ended_pct,rotation_ended_t):
        self.rotating_pct = rotating_pct
        self.rotating_t = rotating_t
        self.rotation_ended_pct = rotation_ended_pct
        self.rotation_ended_t = rotation_ended_t
        

