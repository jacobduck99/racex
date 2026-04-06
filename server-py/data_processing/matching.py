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
            if speed["speed_pct"] >= corner.rotating_pct and speed["speed_pct"] <= corner.rotation_ended_pct:
                if speed["current_speed"] < min_speed:
                    min_speed = speed["current_speed"]
        corner.min_speed = convert_to_kph(min_speed)
        min_speed = float('inf')

def populate_corners(corners, throttle, braking, spd):
    match_braking_to_corners(corners, braking)
    match_throttle_to_corners(corners, throttle)
    min_speed_at_apex(spd, corners)

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
