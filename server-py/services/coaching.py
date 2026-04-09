from services.utils import convert_to_meters
from services.brake_coaching import BrakeCoaching
from services.gear_coaching import GearCoaching
from services.throttle_coaching import ThrottleCoaching

def coaching(corners, lap_dist):
    brake = BrakeCoaching(corners, lap_dist)
    gear = GearCoaching(corners)
    throttle = ThrottleCoaching(corners, lap_dist)
    
    brake_tips = {b["sector"]: b["braking"] for b in brake.coaching_brake_tips()}
    gear_tips = {g["sector"]: g["gear"] for g in gear.coaching_gear_tips()}
    throttle_tips = {t["sector"]: t["throttle"] for t in throttle.coaching_throttle_tips()}
 
    all_sectors = sorted(set(brake_tips) | set(gear_tips) | set(throttle_tips))
    
    deltas = []
    for d in corners:
        deltas.append(d.delta)

    coaching_by_corners = []
    for sector in all_sectors:
        entry = {"sector": sector}
        if sector in brake_tips:
            entry["braking"] = brake_tips[sector]
        if sector in gear_tips:
            entry["gear"] = gear_tips[sector]
        if sector in throttle_tips:
            entry["throttle"] = throttle_tips[sector]
        coaching_by_corners.append(entry)

    for i, v in enumerate(coaching_by_corners):
        v["delta"] = deltas[i]
        #v[delta] = i
        #print("list", coaching_by_corners)
    print("coaching", coaching_by_corners)

    return coaching_by_corners    
