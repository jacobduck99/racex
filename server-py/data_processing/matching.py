from services.utils import convert_to_kph
from data_processing.corner import Matched

def populate_brake_zones(corners, braking):
    for corner in corners:
        for brake_zone in braking:
            if brake_zone.brake_on_pct >= corner.rotating_pct - 0.05 and brake_zone.brake_off_pct <= corner.rotation_ended_pct: 
                corner.brake_zone = brake_zone
                braking.remove(brake_zone)
                break

def populate_throttle_zones(corners, throttle):
    copy_brake_list = corners.copy()

    for corner in copy_brake_list:
        for detected_throttle in throttle:
            if detected_throttle.throttle_off_pct >= corner.rotating_pct - 0.05 and detected_throttle.throttle_off_pct <= corner.rotation_ended_pct:
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
            if min_gear is None:
                min_gear = gear["current_gear"]
            if gear["pct"] >= corner.rotating_pct and gear["pct"] <= corner.rotation_ended_pct:
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
            if abs(fast_zones.rotating_pct - ref_zones.rotating_pct) <= 0.05:
                seen_ref_corners.append(ref_zones)
                matched_zones.append(
                    Matched(fast=fast_zones,
                            ref=ref_zones, corner_num=None)
                )
                break
    for i, c in enumerate(matched_zones, start=1):
        c.corner_num = i
    return matched_zones
