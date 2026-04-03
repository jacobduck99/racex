from services.corner_detection import CornerDetector, Corner, Brake, Matched
import json

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

def match_zones(fast_lap, reference_lap):
    seen_ref_corners = []
    matched_zones = []
    for fast_zones in fast_lap:
        for reference_zones in reference_lap:
            if reference_zones in seen_ref_corners:
                continue
            if fast_zones.brake_zone is None and reference_zones.brake_zone is None:
                if abs(fast_zones.rotating_pct - reference_zones.rotating_pct) <= 0.05:
                    seen_ref_corners.append(reference_zones)
                    matched_zones.append(
                        Matched(fast=fast_zones,
                                ref=reference_zones)
                    )
                    break 

            elif fast_zones.brake_zone is not None and reference_zones.brake_zone is not None and abs(fast_zones.brake_zone.brake_on_pct - reference_zones.brake_zone.brake_on_pct) <= 0.05:
                    seen_ref_corners.append(reference_zones)
                    matched_zones.append(
                        Matched(fast=fast_zones,
                                ref=reference_zones, corner_num=None)
                    )
                    break
    for i, c in enumerate(matched_zones, start=1):
        c.corner_num = i
    return matched_zones

def analyse_lap(lap, rotation=0.3, not_rotating=0.3, brake_on_threshold=0.05, brake_off_threshold=0.05, throttle_on_threshold=0.1, throttle_off_threshold=0.2):
    corner = CornerDetector()

    for sample in lap:
        yaw_rate = sample["yawRate"]
        pct = sample["pct"]
        t = sample["t"]
        b = sample["brake"]
        throttle = sample["throttle"]
        spd = sample["speed"]
        gear = sample["gear"]

        corner.min_speed(spd, pct)

        if abs(yaw_rate) >= rotation:
            corner.open_corner(pct, t, yaw_rate)
        elif abs(yaw_rate) <= not_rotating:
            corner.close_corner(pct, t, corner.min_speed_kph, yaw_rate)
        
        if b >= brake_on_threshold:
            corner.brake_on(pct, t, b)
            corner.max_brake(b)
        elif b <= brake_off_threshold:
            corner.brake_off(pct, t, b)

        if throttle > throttle_on_threshold:
            corner.throttle_on(pct, t, throttle, gear)
        elif throttle < throttle_off_threshold:
            corner.throttle_off(pct, t, throttle)
    clean = corner.filter_corners(corner.corners) 
    merged = corner.merge_corner(clean)
    print("here's whats merged", len(merged))
    
    braking_matched = match_braking_to_corners(merged, corner.brake_zones)
    throttle_matched = match_throttle_to_corners(merged, corner.throttle)
    return throttle_matched
