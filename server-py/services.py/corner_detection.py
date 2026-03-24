
class CornerDetector:
    def __init__(self, yaw_rate):
        self.yaw_rate = yaw_rate
        self.car_rotating = False

    def open_corner(self, pct, t):
        self.car_rotating = True
        self.rotating_pct = pct
        self.rotating_t = t

    def close_corner(self, pct, t):
        self.car_rotating = False
        self.rotating_ended_pct = pct
        self.rotating_ended_t = t

