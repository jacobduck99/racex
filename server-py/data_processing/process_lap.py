from data_processing.corner_detection import CornerDetection
from data_processing.brake_detection import BrakeDetection, Brake
from data_processing.throttle_detection import ThrottleDetection, Throttle
from data_processing.corner import Matched
import json

from services.utils import convert_to_kph

def match_braking_to_corners(corners, braking):
    matched_corners = []

    for corner in corners:
        for brake_zone in braking:
            if brake_zone.brake_on_pct >= corner.rotating_pct - 0.05 and brake_zone.brake_off_pct <= corner.rotation_ended_pct: 
                corner.brake_zone = brake_zone
                braking.remove(brake_zone)
                break
        matched_corners.append(corner)
    return matched_corners

def match_throttle_to_corners(corners, throttle):
    matched_corners = []
    copy_brake_list = corners.copy()

    for corner in copy_brake_list:
        for detected_throttle in throttle:
            if detected_throttle.throttle_off_pct >= corner.rotating_pct - 0.05 and detected_throttle.throttle_off_pct <= corner.rotation_ended_pct:
                corner.throttle = detected_throttle  
                throttle.remove(detected_throttle)
                break
        matched_corners.append(corner)
    return matched_corners

def min_speed_at_apex(spd, corners):
    min_speed = float('inf')
    for corner in corners:
        for speed in spd:
            if speed["speed_pct"] >= corner.rotating_pct and speed["speed_pct"] <=corner.rotation_ended_pct:
                if speed["current_speed"] < min_speed:
                    min_speed = speed["current_speed"]
        corner.min_speed = convert_to_kph(min_speed)
        min_speed = float('inf')

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

def analyse_lap(lap, rotation=0.3, not_rotating=0.3, brake_on_threshold=0.05, brake_off_threshold=0.05, throttle_on_threshold=0.1, throttle_off_threshold=0.2):
    corner = CornerDetection()
    brake = BrakeDetection()
    throttle = ThrottleDetection()

    speed_samples = []

    for sample in lap:
        yaw_rate = sample["yawRate"]
        pct = sample["pct"]
        t = sample["t"]
        b = sample["brake"]
        throttle_val = sample["throttle"]
        spd = sample["speed"]
        gear = sample["gear"]

        speed_samples.append({"current_speed": spd, "speed_pct": pct})

        if abs(yaw_rate) >= rotation:
            corner.open_corner(pct, t, yaw_rate)
        elif abs(yaw_rate) <= not_rotating:
            corner.close_corner(pct, t, yaw_rate)
        
        if b >= brake_on_threshold:
            brake.brake_on(pct, t, b)
            brake.max_brake(b)
        elif b <= brake_off_threshold:
            brake.brake_off(pct, t, b)

        if throttle_val > throttle_on_threshold:
            throttle.throttle_on(pct, t, throttle_val, gear)
        elif throttle_val < throttle_off_threshold:
            throttle.throttle_off(pct, t, throttle_val)

    merged = corner.merge_corner(corner.corners)
    clean = corner.filter_corners(merged) 
    braking_matched = match_braking_to_corners(clean, brake.brake_zones)
    throttle_matched = match_throttle_to_corners(clean, throttle.throttle_inputs)
    get_min_speed = min_speed_at_apex(speed_samples, throttle_matched)
    return throttle_matched
