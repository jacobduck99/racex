from services.corner_detection import CornerDetector, Corner, Brake
import json

def detect_corners(lap, rotation=0.3, not_rotating=0.03):
    corner = CornerDetector()
    for sample in lap:
        yaw_rate = sample["yawRate"]
        pct = sample["pct"]
        t = sample["t"]

        if abs(yaw_rate) >= rotation:
            corner.open_corner(pct, t)
        elif abs(yaw_rate) <= not_rotating:
            corner.close_corner(pct, t)
    return corner.corners

def detect_brake_zones(lap, brake_on_threshold=0.05, brake_off_threshold=0.05):
    brake = CornerDetector()
    for sample in lap:
        b = sample["brake"]
        pct = sample["pct"]
        t = sample["t"]

        if b >= brake_on_threshold:
            brake.brake_on(pct, t, b)
        elif b <= brake_off_threshold:
            brake.brake_off(pct, t, b)
    return brake.brake_zones

def match_braking_to_corners1(lap):
    corners = detect_corners(lap)
    braking = detect_brake_zones(lap)

    matched_corners = []

    for corner in corners:
        for brake_zone in braking:
            if brake_zone.brake_on_pct >= corner.rotating_pct - 0.05and brake_zone.brake_off_pct <= corner.rotation_ended_pct: 
                corner.brake_zone = brake_zone
                braking.remove(brake_zone)
                break
        matched_corners.append(corner)
    print("here's matched corners brake and corners", matched_corners)
    return matched_corners





