from services.utils import convert_to_meters
from services.brake_coaching import BrakeCoaching

def coaching(corners, lap_dist):
    brake = BrakeCoaching(corners, lap_dist)
    brake.coaching_brake_tips()
    
