from services.utils import convert_to_kph
from data_processing.corner import Matched

# Distances are fractions of a lap (see corner_detection.py).
# Braking / lifting can start this far before the car begins to rotate and still belong to that corner.
CORNER_ENTRY_WINDOW_PCT = 0.05
# A fast-lap corner and a reference corner this close together are the same corner.
CORNER_MATCH_PCT = 0.05

def populate_brake_zones(corners, braking):
    # removing inside the loop is safe only because we break straight after
    for corner in corners:
        for brake_zone in braking:
            if brake_zone.brake_on_pct >= corner.rotating_pct - CORNER_ENTRY_WINDOW_PCT and brake_zone.brake_off_pct <= corner.rotation_ended_pct:
                corner.brake_zone = brake_zone
                braking.remove(brake_zone)
                break

def populate_throttle_zones(corners, throttle):
    for corner in corners:
        for detected_throttle in throttle:
            if detected_throttle.throttle_off_pct >= corner.rotating_pct - CORNER_ENTRY_WINDOW_PCT and detected_throttle.throttle_off_pct <= corner.rotation_ended_pct:
                corner.throttle = detected_throttle  
                throttle.remove(detected_throttle)
                break

def populate_min_speed(spd, corners):
    min_speed = float('inf')
    for corner in corners:
        for speed in spd:
            if speed["speed_pct"] >= corner.rotating_pct and speed["speed_pct"] <= corner.rotation_ended_pct:
                if speed["current_speed"] < min_speed:
                    min_speed = speed["current_speed"]
        corner.min_speed = convert_to_kph(min_speed)
        min_speed = float('inf')

def populate_gear_in_corner(gears, corners):
    min_gear = None
    for corner in corners:
        for gear in gears:
            if gear["current_gear"] == 0:
                continue
            if gear["pct"] >= corner.rotating_pct and gear["pct"] <= corner.rotation_ended_pct:
                if min_gear is None:
                    min_gear = gear["current_gear"]
                if gear["current_gear"] < min_gear: 
                    min_gear = gear["current_gear"]
        corner.gear = min_gear
        min_gear = None

def populate_corners(corners, throttle, braking, spd, gears):
    populate_brake_zones(corners, braking)
    populate_throttle_zones(corners, throttle)
    populate_min_speed(spd, corners)
    populate_gear_in_corner(gears, corners)
    
def match_zones(fast_lap, ref_lap):
    seen_ref_corners = []
    matched_zones = []
    for fast_zones in fast_lap:
        for ref_zones in ref_lap:
            if ref_zones in seen_ref_corners:
                continue
            if abs(fast_zones.rotating_pct - ref_zones.rotating_pct) <= CORNER_MATCH_PCT:
                seen_ref_corners.append(ref_zones)
                # - means fast quicker + means ref faster
                fast_corner_time = fast_zones.rotation_ended_t - fast_zones.rotating_t
                ref_corner_time = ref_zones.rotation_ended_t - ref_zones.rotating_t
                delta = ref_corner_time - fast_corner_time
                rounded = round(delta, 3)
                matched_zones.append(
                    Matched(fast=fast_zones,
                            ref=ref_zones, fast_corner_time=fast_corner_time, ref_corner_time=ref_corner_time, delta=rounded, corner_num=None)
                )
                break
    for i, c in enumerate(matched_zones, start=1):
        c.corner_num = i
    return matched_zones
