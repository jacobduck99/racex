from data_processing.corner_detection import CornerDetection
from data_processing.brake_detection import BrakeDetection, Brake
from data_processing.throttle_detection import ThrottleDetection, Throttle
from data_processing.matching import populate_corners

def analyse_lap(lap, rotation=0.3, not_rotating=0.3, brake_on_threshold=0.05, brake_off_threshold=0.05, throttle_on_threshold=0.1, throttle_off_threshold=0.2):
    corner = CornerDetection()
    brake = BrakeDetection()
    throttle = ThrottleDetection()

    speed_samples = []

    for sample in lap:
        yaw_rate = sample["yawRate"]
        pct = sample["pct"]
        t = sample["t"]
        b = sample["brake"]
        throttle_val = sample["throttle"]
        spd = sample["speed"]
        gear = sample["gear"]

        speed_samples.append({"current_speed": spd, "speed_pct": pct})

        if abs(yaw_rate) >= rotation:
            corner.open_corner(pct, t, yaw_rate)
            corner.set_apex(yaw_rate, gear)
        elif abs(yaw_rate) <= not_rotating:
            corner.close_corner(pct, t, yaw_rate)
        
        if b >= brake_on_threshold:
            brake.brake_on(pct, t, b)
            brake.max_brake(b)
        elif b <= brake_off_threshold:
            brake.brake_off(pct, t, b)

        if throttle_val > throttle_on_threshold:
            throttle.throttle_on(pct, t, throttle_val, gear)
        elif throttle_val < throttle_off_threshold:
            throttle.throttle_off(pct, t, throttle_val)

    merged = corner.merge_corner(corner.corners)
    clean = corner.filter_corners(merged) 
    populate_corners(clean, throttle.throttle_inputs,brake.brake_zones, speed_samples)
    print("here's clean object", clean)
    return clean

