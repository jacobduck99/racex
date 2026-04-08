from services.utils import convert_to_kph, convert_to_meters

class ThrottleCoaching:
    def __init__(self, corners, lap_dist):
        self.corners = corners
        self.lap_dist = lap_dist
        self.coaching = []

    def coaching_throttle_tips(self):
        for t in self.corners:
            fast_throttle = t.fast.throttle
            ref_throttle = t.ref.throttle
            sector = t.corner_num
            if fast_throttle is None or ref_throttle is None:
                continue
            distance = abs(fast_throttle.throttle_on_pct - ref_throttle.throttle_on_pct)
            meters = int(convert_to_meters(self.lap_dist, distance))
            check_meters = "meter" if meters == 1 else "meters"
            if meters == 0:
                tip = f"Sector {sector}: Throttle application matches your fastest lap. Consistent."
            elif ref_throttle.throttle_on_pct < fast_throttle.throttle_on_pct:
                if meters <= 3:
                    tip = f"Sector {sector}: Getting on throttle {meters} {check_meters} early — close to your best. Stay disciplined."
                else:
                    tip = f"Sector {sector}: Getting on throttle {meters} {check_meters} early — rushing the exit. Wait for the car to rotate before applying power."
            else:
                if meters <= 3:
                    tip = f"Sector {sector}: Getting on throttle {meters} {check_meters} late — minor hesitation. Trust the grip."
                else:
                    tip = f"Sector {sector}: Getting on throttle {meters} {check_meters} late — leaving time on the table. Pick up the throttle earlier to maximise exit speed."
            self.coaching.append({"Sector": sector, "throttle": tip})
        print("James says", self.coaching)

        return self.coaching




