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

def find_corners_by_yaw_rate2(lap, rotation=0.3, not_rotating=0.03):
    car_rotating = False
    current = None
    corner = []
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
            corner.append(current)
            current = None

    for i in range(len(corner) - 1):
        current = corner[i]
        print("current", current)
        next_one = corner[i + 1]
        print("next_one", next_one)

    print("here's your corners", corner)
        
    














def find_corners_by_yaw_rate(lap, yaw_rate_on=0.03, yaw_rate_off=0.03, min_corner_duration=0.5, yaw_rate_dip_duration_s=0.5, yaw_rate_flipped_duration=1):
    current = None
    turns = []
    car_rotating = False
    yaw_rate_dip = None
    yaw_rate_flipped = None
    previous_yaw_rate = None
    for sample in lap:
        yaw_rate = sample["yawRate"]
        pct = sample["pct"]
        t = sample["t"]
        if not car_rotating and abs(yaw_rate) >= yaw_rate_on:
            car_rotating = True
            yaw_rate_dip = None
            current = {
                "yaw_rate": yaw_rate,
                "pct": pct,
                "t": t,
                "car_rotating_on_pct": pct,
                "car_rotating_on_t": t,
                "car_rotating_off_pct": None,
                "car_rotating_off_t": None,
            }
        elif car_rotating and previous_yaw_rate is not None and previous_yaw_rate * yaw_rate < 0 and abs(yaw_rate) >= yaw_rate_on:
            yaw_rate_flipped = t
            if car_rotating and yaw_rate_flipped is not None and (t - yaw_rate_flipped) >= yaw_rate_flipped_duration:
                current["car_rotating_off_pct"] = pct
                current["car_rotating_off_t"] = t
                current["duration_of_rotation_s"] = t - current["car_rotating_on_t"]
                if current["duration_of_rotation_s"] >= min_corner_duration:
                    turns.append(current)
            yaw_rate_dip = None
            current = {
                "yaw_rate": yaw_rate,
                "pct": pct,
                "t": t,
                "car_rotating_on_pct": pct,
                "car_rotating_on_t": t,
                "car_rotating_off_pct": None,
                "car_rotating_off_t": None,
            }
        elif car_rotating and abs(yaw_rate) >= yaw_rate_on:
            yaw_rate_dip = None
        elif car_rotating and abs(yaw_rate) < yaw_rate_off and yaw_rate_dip is None:
            yaw_rate_dip = t
        elif car_rotating and yaw_rate_dip is not None and (t - yaw_rate_dip) >= yaw_rate_dip_duration_s:
            current["car_rotating_off_pct"] = pct
            current["car_rotating_off_t"] = t
            current["duration_of_rotation_s"] = t - current["car_rotating_on_t"]
            car_rotating = False
            if current["duration_of_rotation_s"] >= min_corner_duration:
                turns.append(current)
            current = None
            yaw_rate_dip = None
        previous_yaw_rate = yaw_rate
    if car_rotating and current is not None and lap:
        last = lap[-1]
        current["car_rotating_off_pct"] = last["pct"]
        current["car_rotating_off_t"] = last["t"]
        current["duration_of_rotation_s"] = current["car_rotating_off_t"] - current["car_rotating_on_t"]
        if current["duration_of_rotation_s"] >= min_corner_duration:
            turns.append(current)
        current = None
        car_rotating = False
    turns.sort(key=lambda c: c["car_rotating_on_pct"])
    for i, c in enumerate(turns, start=1):
        c["corner_num"] = i
    print("Here are your turns in order", json.dumps(turns, indent=2))
    return {
        "found": len(turns) > 0,
        "turns": turns,
    }

def build_corner_map(lap):
    find_corners_yaw_rate = find_corners_by_yaw_rate(lap)
    #print("Yaw rate", find_corners_yaw_rate["turns"][0])
    find_braking = find_brake_zones(lap)
    detected_brake_zones = find_braking.get("corners", [])
    # pretty_dump = json.dumps(detected_brake_zones, indent=2)
    # print("here's your dump", pretty_dump)
    corners = find_corners_yaw_rate.get("turns", [])
    # print("here's your corners", corners)
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
            brake_zone["car_rotating_on_pct"] = best_match["car_rotating_on_pct"]
            brake_zone["car_rotating_off_pct"] = best_match["car_rotating_off_pct"]
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
                
