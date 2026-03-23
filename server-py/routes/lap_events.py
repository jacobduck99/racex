import json

#pct means distance around track 
# lots of comments because this is complex 

def convert_to_kph(speed):
    speed_in_kph = speed * 3.6
    return speed_in_kph

def find_brake_zones(lap, threshold=0.05, throttle_off_threshold=0.2, throttle_on_threshold=0.1):
    corners = []
    braking = False
    current = None
    throttle_off_t = None

    for sample in lap:
        b = sample["brake"]
        spd = sample["speed"]
        pct = sample["pct"]
        t = sample["t"]
        steering = sample["steering"]
        throttle = sample["throttle"]

        if not braking:
            if throttle > throttle_on_threshold:
                throttle_off_t = None
            elif throttle_off_t is None and throttle <= throttle_off_threshold:
                throttle_off_t = t

        # Brake turns ON
        if not braking and b >= threshold:
            # close previous zone if it never got a throttle-on
            if current is not None and current["brake_off_t"] is not None:
                current["throttle_on_pct"] = None
                current["zone_pct"] = current["brake_off_pct"] - current["brake_on_pct"]
                if current["zone_pct"] < 0:
                    current["zone_pct"] += 1.0
                corners.append(current)
                current = None
                throttle_off_t = None  # was throttle_on_t = None (bug)

            braking = True
            current = {
                "brake_on_pct": pct,
                "brake_on_t": t,
                "brake_off_pct": None,
                "brake_off_t": None,
                "max_brake": b,
                "max_brake_pct": pct,
                "max_speed": spd,
                "max_speed_kph": convert_to_kph(spd),
                "max_speed_pct": pct,
                "min_speed": spd,
                "min_speed_kph": convert_to_kph(spd),  # was missing
                "min_speed_pct": pct,
                "steering_samples": [],
                "throttle_off_t": throttle_off_t,
                "throttle_on_t": None,
                "coast_duration_s": None,  # set at close, not here
            }
            current["steering_samples"].append({"pct": pct, "t": t, "steering": steering, "throttle": throttle})
            continue

        if not braking:
            continue

        if spd < current["min_speed"]:
            current["min_speed"] = spd
            current["min_speed_pct"] = pct
            current["min_speed_kph"] = convert_to_kph(spd)

        current["steering_samples"].append({"pct": pct, "t": t, "steering": steering})

        if b > current["max_brake"]:
            current["max_brake"] = b
            current["max_brake_pct"] = pct

        if spd > current["max_speed"]:
            current["max_speed"] = spd
            current["max_speed_pct"] = pct
            current["max_speed_kph"] = convert_to_kph(spd)

        # Brake turns OFF
        if b < threshold:
            braking = False
            current["brake_off_pct"] = pct
            current["brake_off_t"] = t
            current["duration_s"] = current["brake_off_t"] - current["brake_on_t"]

        # Throttle back on — close the zone properly
        if current is not None and current["brake_off_t"] is not None and current["throttle_on_t"] is None and throttle >= throttle_on_threshold:
            current["throttle_on_t"] = t
            current["throttle_on_pct"] = pct
            current["coast_duration_s"] = t - current["brake_off_t"]
            current["zone_pct"] = pct - current["brake_on_pct"]
            if current["zone_pct"] < 0:
                current["zone_pct"] += 1.0
            corners.append(current)
            current = None
            throttle_off_t = None

    for i, c in enumerate(corners, start=1):
        c["corner_num"] = i
    #print("Here's your corners", json.dumps(corners, indent=2))

    return {
        "found": len(corners) > 0,
        "corners": corners,
    }

def find_corners_by_yaw_rate(lap, rotation=0.3, not_rotating=0.03):
    car_rotating = False
    current = None
    previous_corner = None
    merged_corners = []
    corners = []
    for sample in lap:
        yaw_rate = sample["yawRate"]
        pct = sample["pct"]
        t = sample["t"]
        #turn on rotation 
        if not car_rotating and abs(yaw_rate) >= rotation:
            car_rotating = True
            current = {
                "yaw_rate": yaw_rate,
                "pct": pct,
                "t": t,
                "rotation_started_pct": pct,
                "rotation_started_t": t,
                "rotation_ended_pct": None,
                "rotation_ended_t": None,
            }

        elif car_rotating and abs(yaw_rate) <= not_rotating:
            car_rotating = False
            current["rotation_ended_pct"] = pct
            current["rotation_ended_t"] = t
            corners.append(current)
            current = None

    for next_corner in corners:
        #First iteration sets the current_corner
        if previous_corner is None:
            previous_corner = next_corner
        else:
            #compare current corner to corners loop
            time_to_next_corner = previous_corner["rotation_ended_t"] - next_corner["rotation_started_t"]
            if time_to_next_corner < 0.5 and previous_corner["yaw_rate"] * next_corner["yaw_rate"] > 0:
                previous_corner["rotation_ended_t"] = next_corner["rotation_ended_t"]
            else:
                merged_corners.append(previous_corner)
                previous_corner = next_corner
    merged_corners.append(previous_corner)
    print("Merged corners:", merged_corners)
    return {
        "found": len(merged_corners) > 0,
        "turns": merged_corners,
    }

def match_braking_to_corners(lap):
    corners_yaw_rate = find_corners_by_yaw_rate(lap)
    braking = find_brake_zones(lap)
    detected_brake_zones = braking.get("corners", [])
    corners = corners_yaw_rate.get("merged_corners", [])

    match_corner = []

    for brake_zone in detected_brake_zones:
        

def build_corner_map(lap):
    find_corners_yaw_rate = find_corners_by_yaw_rate(lap)
    #print("Yaw rate", find_corners_yaw_rate["turns"][0])
    find_braking = find_brake_zones(lap)
    detected_brake_zones = find_braking.get("corners", [])
    # pretty_dump = json.dumps(detected_brake_zones, indent=2)
    # print("here's your dump", pretty_dump)
    corners = find_corners_yaw_rate.get("merged_corners", [])
    # print("here's your corners", corners)
    matched_brake_zones = []
    
    for brake_zone in detected_brake_zones: 
        best_match = None
        best_distance = float("inf")
        for corner in corners:
            if brake_zone["brake_on_pct"] >= corner["rotation_started_pct"] - 0.05 and brake_zone["brake_on_pct"] <= corner["rotation_ended_pct"]:
                distance = abs(brake_zone["brake_on_pct"] - corner["rotation_started_pct"])
                if distance < best_distance:
                    best_distance = distance
                    best_match = corner
        if best_match is not None:
            brake_zone["car_rotating_on_pct"] = best_match["rotation_started_pct"]
            brake_zone["car_rotating_off_pct"] = best_match["rotation_ended_pct"]
            brake_zone["yaw_rate"] = best_match["yaw_rate"]
            brake_zone["duration_of_rotation_s"] = best_match["duration_of_rotation_s"]
            matched_brake_zones.append(brake_zone)
                     
    return matched_brake_zones

def match_zones(fast_lap, reference_lap):
    matched_zones = []
    for fast_zones in fast_lap:
        for reference_zones in reference_lap:
            if abs(fast_zones["car_rotating_on_pct"] - reference_zones["car_rotating_on_pct"]) <= 0.05:
                matched_zones.append({
                    "fast": fast_zones,
                    "reference": reference_zones
                })
                break
    return matched_zones
                
