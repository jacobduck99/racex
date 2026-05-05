from data_processing.corner_detection import CornerDetection
from data_processing.brake_detection import BrakeDetection, Brake
from data_processing.throttle_detection import ThrottleDetection, Throttle
from data_processing.matching import populate_corners

def analyse_lap(lap, track_corners=None, rotation=0.3, not_rotating=0.3, brake_on_threshold=0.05, brake_off_threshold=0.05, throttle_on_threshold=0.1, throttle_off_threshold=0.2):
    corner = CornerDetection()
    brake = BrakeDetection()
    throttle = ThrottleDetection()

    speed_samples = []
    gear_samples = []

    for sample in lap:
        yaw_rate = sample["yawRate"]
        pct = sample["pct"]
        t = sample["t"]
        b = sample["brake"]
        throttle_val = sample["throttle"]
        spd = sample["speed"]
        gear = sample["gear"]
        lon = sample["lon"]
        lat = sample["lat"]

        speed_samples.append({"current_speed": spd, "speed_pct": pct})
        gear_samples.append({"current_gear": gear, "pct": pct})

        if abs(yaw_rate) >= rotation:
            corner.open_corner(pct, t, yaw_rate, lon, lat)
        elif abs(yaw_rate) <= not_rotating:
            corner.close_corner(pct, t, yaw_rate, lon, lat)
        
        if b >= brake_on_threshold:
            brake.brake_on(pct, t, b)
            brake.max_brake(b)
        elif b <= brake_off_threshold:
            brake.brake_off(pct, t, b)

        if throttle_val > throttle_on_threshold:
            throttle.throttle_on(pct, t, throttle_val)
        elif throttle_val < throttle_off_threshold:
            throttle.throttle_off(pct, t, throttle_val)
#    for i, c in enumerate(corner.corners, start=1):
    #    print("raw r start", c.rotating_pct, "raw r end", c.rotation_ended_pct, "corner num", i)
    # make for loop print("lap not merged", corner.corners.rotating_pct)
    merged = corner.merge_corner(corner.corners)
    #for i, m in enumerate(merged, start=1):
    #    print("merged", "r start", m.rotating_pct, "r end", m.rotation_ended_pct, "corner num", i)
    clean = corner.filter_corners(merged, track_corners) 
    #for i, m in enumerate(clean, start=1):
    #    print("cleaned", "rotating start", m.rotating_pct, "rotation ended", m.rotation_ended_pct, "yaw_rate", m.yaw_rate, "corner num", i)
    populate_corners(clean, throttle.throttle_inputs,brake.brake_zones, speed_samples, gear_samples)
    return clean


