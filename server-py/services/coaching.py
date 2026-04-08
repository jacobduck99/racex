from services.utils import convert_to_meters
from services.brake_coaching import BrakeCoaching
from services.gear_coaching import GearCoaching
from services.throttle_coaching import ThrottleCoaching

def coaching(corners, lap_dist):
    brake = BrakeCoaching(corners, lap_dist)
    gear = GearCoaching(corners) 
    throttle = ThrottleCoaching(corners, lap_dist)
    brake.coaching_brake_tips()
    gear.coaching_gear_tips()
    throttle.coaching_throttle_tips()
    
