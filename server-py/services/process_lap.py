from services.corner_detection import CornerDetector, Corner, Brake
import json

def convert_to_kph1(speed):
    speed_in_kph = speed * 3.6
    return speed_in_kph

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

    for corner in corners:
        for detected_throttle in throttle:
            if detected_throttle.throttle_off_pct >= corner.rotating_pct - 0.05 and detected_throttle.throttle_off_pct <= corner.rotation_ended_pct:
                corner.throttle = detected_throttle  
                throttle.remove(detected_throttle)
                break
        matched_corners.append(corner)
    return matched_corners


def analyse_lap(lap, rotation=0.3, not_rotating=0.03, brake_on_threshold=0.05, brake_off_threshold=0.05, throttle_on_threshold=0.1, throttle_off_threshold=0.2):
    corner = CornerDetector()
    for sample in lap:
        yaw_rate = sample["yawRate"]
        pct = sample["pct"]
        t = sample["t"]
        b = sample["brake"]
        throttle = sample["throttle"]
        speed = sample["speed"]
        gear = sample["gear"]

        if abs(yaw_rate) >= rotation:
            corner.open_corner(pct, t)
        elif abs(yaw_rate) <= not_rotating:
            corner.close_corner(pct, t)
        
        if b >= brake_on_threshold:
            corner.brake_on(pct, t, b)
        elif b <= brake_off_threshold:
            corner.brake_off(pct, t, b)

        if throttle > throttle_on_threshold:
            corner.throttle_on(pct, t, throttle, gear)
        elif throttle < throttle_off_threshold:
            corner.throttle_off(pct, t, throttle)

    braking_matched = match_braking_to_corners(corner.corners, corner.brake_zones)
    throttle_matched = match_throttle_to_corners(corner.corners, corner.throttle)
    print("here's matched", throttle_matched)
    return throttle_matched



