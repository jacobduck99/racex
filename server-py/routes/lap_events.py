#pct means distance around track 
# lots of comments because this is complex 

def convert_to_kph(speed):
    speed_in_kph = speed * 3.6
    return speed_in_kph

def find_brake_zones(lap, threshold=0.05, throttle_off_threshold=0.2, throttle_on_threshold=0.8):
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
                throttle_off_t = None  # driver back on throttle, reset
            elif throttle_off_t is None and throttle <= throttle_off_threshold:
                throttle_off_t = t  # driver just lifted, start tracking

        # Brake turns ON start a new zone
        if not braking and b >= threshold:
            if current is not None and current["brake_off_t"] is not None:
                zone_pct = current["brake_off_pct"] - current["brake_on_pct"]
                if zone_pct < 0:
                    zone_pct += 1.0
                current["zone_pct"] = zone_pct
                corners.append(current)
                current = None
                throttle_on_t = None
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
                "min_speed_pct": pct,
                "steering_samples": [],
                "coast_duration_s": (t - throttle_off_t) if throttle_off_t is not None else None,
                "throttle_off_t": throttle_off_t,  
                "throttle_on_t": None,
            }
            current["steering_samples"].append({"pct": pct, "t": t, "steering": steering})
            continue

        # If we're not braking, ignore samples
        if not braking:
            continue
        
        # We are braking: record sample + update min/max
        if spd < current["min_speed"]:
            current["min_speed"] = spd 
            current["min_speed_pct"] = pct
            spd_in_kph = convert_to_kph(current["min_speed"])
            current["min_speed_kph"] = spd_in_kph

        current["steering_samples"].append({"pct": pct, "t": t, "steering": steering})

        if b > current["max_brake"]:
            current["max_brake"] = b
            current["max_brake_pct"] = pct

        if spd > current["max_speed"]:
            current["max_speed"] = spd
            current["max_speed_pct"] = pct
            spd_in_kph = convert_to_kph(current["max_speed"])
            current["max_speed_kph"] = spd_in_kph

        # Brake turns OFF
        if b < threshold:
            braking = False
            current["brake_off_pct"] = pct
            current["brake_off_t"] = t
            current["duration_s"] = current["brake_off_t"] - current["brake_on_t"]

        if current is not None and current["brake_off_t"] is not None and current["throttle_on_t"] is None and throttle >= threshold:
            current["throttle_on_t"] = t
            
            zone_pct = current["brake_off_pct"] - current["brake_on_pct"]
            if zone_pct < 0:
                zone_pct += 1.0
            current["zone_pct"] = zone_pct
            corners.append(current)
            current = None
            throttle_on_t = None
            throttle_off_t = None  # reset for the next zone

    # number them in order
    for i, c in enumerate(corners, start=1):
        c["corner_num"] = i

    return {
        "found": len(corners) > 0,
        "corners": corners,
    }

def find_corners_by_yaw_rate(lap, on_threshold=0.03, off_threshold=0.02, min_duration_s=0.3):
    current = None
    turns = []
    car_rotating = False

    for sample in lap:
        yaw_rate = sample["yawRate"]
        pct = sample["pct"]
        t = sample["t"]

        if not car_rotating and abs(yaw_rate) >= on_threshold:
            car_rotating = True
            current = {
                "yaw_rate": yaw_rate,
                "pct": pct,
                "t": t,
                "car_rotating_on_pct": pct,
                "car_rotating_on_t": t,
                "car_rotating_off_pct": None,
                "car_rotating_off_t": None,
            }

        if car_rotating and abs(yaw_rate) < off_threshold:
            car_rotating = False
            current["car_rotating_off_pct"] = pct
            current["car_rotating_off_t"] = t
            current["duration_of_rotation_s"] = current["car_rotating_off_t"] - current["car_rotating_on_t"]

            if current["duration_of_rotation_s"] >= min_duration_s:
                turns.append(current)

            current = None

    if car_rotating and current is not None and lap:
        last = lap[-1]
        current["car_rotating_off_pct"] = last["pct"]
        current["car_rotating_off_t"] = last["t"]
        current["duration_of_rotation_s"] = current["car_rotating_off_t"] - current["car_rotating_on_t"]

        if current["duration_of_rotation_s"] >= min_duration_s:
            turns.append(current)

        current = None
        car_rotating = False

    turns.sort(key=lambda c: c["car_rotating_on_pct"])
    for i, c in enumerate(turns, start=1):
        c["corner_num"] = i

    return {
        "found": len(turns) > 0,
        "turns": turns,
    }

def build_corner_map(lap):
    find_corners_yaw_rate = find_corners_by_yaw_rate(lap)
    find_braking = find_brake_zones(lap)
    detected_brake_zones = find_braking.get("corners", [])
    corners = find_corners_yaw_rate.get("turns", [])
    matched_brake_zones = []
    
    for brake_zone in detected_brake_zones: 
        best_match = None
        best_distance = float("inf")
        for corner in corners:
            if brake_zone["brake_on_pct"] >= corner["car_rotating_on_pct"] - 0.05 and brake_zone["brake_on_pct"] <= corner["car_rotating_off_pct"]:
                distance = abs(brake_zone["brake_on_pct"] - corner["car_rotating_on_pct"])
                if distance < best_distance:
                    best_distance = distance
                    best_match = corner
        if best_match is not None:
            brake_zone["best_match"] = best_match
            matched_brake_zones.append(brake_zone)
                     
    return  matched_brake_zones

def match_zones(fast_lap, reference_lap):
    matched_zones = []
    for fast_zones in fast_lap:
        for reference_zones in reference_lap:
            if abs(fast_zones["best_match"]["pct"] - reference_zones["best_match"]["pct"]) <= 0.05:
                matched_zones.append({
                    "fast": fast_zones,
                    "reference": reference_zones
                })
                break
    return matched_zones
                
