
class Corner:
    def __init__(self, pct, t, brake, yaw_rate):
        self.pct = []
        self.t = []
        self.brake = []
        self.yaw_rate = []
        self.car_rotating = False
        self.rotating_t = None
        self.rotating_pct = None
        self.not_rotating_t = None
        self.not_rotating_pct = None

    def cornering(self, pct, t):
        self.car_rotating = True
        self.rotating_pct = self.pct
        self.rotating_t = self.t



