
class GearCoaching:
    def __init__(self, corners):
        self.corners = corners

    def coaching_gear_tips(self):
        tips = []
        for corner in self.corners:
            fast_gear = corner.fast.gear
            ref_gear = corner.ref.gear
            sector = corner.corner_num

            if fast_gear is None or ref_gear is None:
                        continue

            if fast_gear == ref_gear:
                tip = f"Gear {ref_gear} matches your fastest laps sector {sector}."
            elif ref_gear < fast_gear:
                tip = f"In gear {ref_gear}, but your fastest was {fast_gear} — shift up."
            else:
                tip = f"In gear {ref_gear}, but your fastest was {fast_gear} — shift down."

            tips.append({"sector": sector, "gear": tip})
        return tips



