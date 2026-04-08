from services.utils import convert_to_meters
from services.brake_coaching import BrakeCoaching
from services.gear_coaching import GearCoaching
from services.throttle_coaching import ThrottleCoaching

def coaching(corners, lap_dist):
    brake = BrakeCoaching(corners, lap_dist)
    gear = GearCoaching(corners)
    throttle = ThrottleCoaching(corners, lap_dist)

    brake_tips = brake.coaching_brake_tips()
    gear_tips = gear.coaching_gear_tips()
    throttle_tips = throttle.coaching_throttle_tips()

    coaching_by_corners = []
    for b, g, t in zip(brake_tips, gear_tips, throttle_tips):
        coaching_by_corners.append({
            "sector": b["Sector"],
            "braking": b["braking"],
            "gear": g["gear"],
            "throttle": t["throttle"],
        })
    print("coaching", coaching_by_corners)
    return coaching_by_corners






    
