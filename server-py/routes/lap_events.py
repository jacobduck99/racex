#pct means distance around track 

def find_brake_zones(lap, threshold=0.05):
    corners = []
    braking = False
    current = None

    for sample in lap:
        b = sample["brake"]
        spd = sample["speed"]
        pct = sample["pct"]
        t = sample["t"]
        steering = sample["steering"]

        # Brake turns ON start a new zone
        if not braking and b >= threshold:
            braking = True
            current = {
                "brake_on_pct": pct,
                "brake_on_t": t,
                "brake_off_pct": None,
                "brake_off_t": None,
                "min_speed": spd,
                "min_speed_pct": pct,
                "steering_samples": [],  # list of {pct,t,steering}
            }
            current["steering_samples"].append({"pct": pct, "t": t, "steering": steering})
            continue

        # If we're not braking, ignore samples
        if not braking:
            continue

        # We are braking record sample + update min speed
        if spd < current["min_speed"]:
            current["min_speed"] = spd
            current["min_speed_pct"] = pct

        current["steering_samples"].append({"pct": pct, "t": t, "steering": steering})

        # Brake turns OFF close the zone
        if b < threshold:
            braking = False
            current["brake_off_pct"] = pct
            current["brake_off_t"] = t

            current["duration_s"] = current["brake_off_t"] - current["brake_on_t"]

            zone_pct = current["brake_off_pct"] - current["brake_on_pct"]
            if zone_pct < 0:
                zone_pct += 1.0
            current["zone_pct"] = zone_pct

            corners.append(current)
            current = None

   #number them in order
    for i, c in enumerate(corners, start=1):
        c["corner_num"] = i

    return {
        "found": len(corners) > 0,
        "corners": corners,
    }
