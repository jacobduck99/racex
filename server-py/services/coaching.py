from services.utils import convert_to_meters
from services.brake_coaching import BrakeCoaching
from services.gear_coaching import GearCoaching

def coaching(corners, lap_dist):
    brake = BrakeCoaching(corners, lap_dist)
    gear = GearCoaching(corners) 
    brake.coaching_brake_tips()
    gear.coaching_gear_tips()
    
