#pct means distance around track 

def find_brake_zone(lap, threshold=0.05):
    brake = False

    brake_on_pct = None
    brake_on_t = None
    brake_off_pct = None
    brake_off_t = None

    min_speed = None

    steering_angle = []

    for sample in lap:
        b = sample["brake"]
        spd = sample["speed"]
        steering = sample["steering"]

        if not brake and b >= threshold:
            brake = True
            brake_on_pct = sample["pct"]
            brake_on_t = sample["t"]
            min_speed = spd
            steering_angle.append(steering)
            continue  # go next sample

        if not brake:
            continue

        if spd < min_speed:
            min_speed = spd
        
        steering_angle.append(steering)

        if b < threshold:
            brake_off_pct = sample["pct"]
            brake_off_t = sample["t"]

            break

    if brake_on_t is None or brake_off_t is None:
        return {
            "found": False,
            "brake_on_pct": brake_on_pct,
            "brake_on_t": brake_on_t,
            "brake_off_pct": brake_off_pct,
            "brake_off_t": brake_off_t,
            "min_speed": min_speed,
            "steering_angle": steering_angle,
        }

    duration_s = brake_off_t - brake_on_t
    zone_pct = brake_off_pct - brake_on_pct

    return {
        "found": True,
        "brake_on_pct": brake_on_pct,
        "brake_on_t": brake_on_t,
        "brake_off_pct": brake_off_pct,
        "brake_off_t": brake_off_t,
        "duration_s": duration_s,
        "zone_pct": zone_pct,
        "min_speed": min_speed,
        "steering_angle": steering_angle,
    }
            
