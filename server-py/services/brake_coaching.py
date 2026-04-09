from services.utils import convert_to_kph, convert_to_meters

class BrakeCoaching:
    def __init__(self, corners, lap_dist):
        self.corners = corners
        self.lap_dist = lap_dist

    def coaching_brake_tips(self):
        tips = []
        for brake_zones in self.corners:
            delta = brake_zones.delta
            fast_brake_zone = brake_zones.fast.brake_zone
            ref_brake_zone = brake_zones.ref.brake_zone
            if fast_brake_zone is None or ref_brake_zone is None:
                continue

            fast_brake_pressure = int(fast_brake_zone.max_brake_pressure * 100)
            ref_brake_pressure = int(ref_brake_zone.max_brake_pressure * 100)
            distance = abs(fast_brake_zone.brake_on_pct - ref_brake_zone.brake_on_pct)
            meters = int(convert_to_meters(self.lap_dist, distance))
            check_meters = "meter" if meters == 1 else "meters"
            sector = brake_zones.corner_num

            if abs(delta) < 0.1:
                tip = "Your approach is working — you are matching your best."
                tips.append({"sector": sector, "braking": tip})
                continue
            if delta < 0:
                tip = "Faster than your best — your braking is working, keep this approach."
                tips.append({"sector": sector, "braking": tip})
                continue
                
            if meters == 0:
                tip = f"Braking at {ref_brake_pressure}% — right on your reference. Clean."
            elif fast_brake_zone.brake_on_pct < ref_brake_zone.brake_on_pct:
                if meters <= 3:
                    tip = f"Braking {meters} {check_meters} early at {ref_brake_pressure}% — consistent with your best. Hold this marker."
                else:
                    tip = f"Braking {meters} {check_meters} early at {ref_brake_pressure}% — over-cautious. Push the brake point deeper."
                    
            else:
                if meters <= 3:
                    tip = f"Braking {meters} {check_meters} late at {ref_brake_pressure}% — minor overshoot. Tighten up the marker."
                else:
                    tip = f"Braking {meters} {check_meters} late at {ref_brake_pressure}% — overshooting your reference. Brake earlier to carry more speed through the corner."

            if fast_brake_pressure < ref_brake_pressure - 10:
                tip += f" Only {fast_brake_pressure}% pressure vs {ref_brake_pressure}% in your best — commit harder."

            tips.append({"sector": sector, "braking": tip})
        return tips
