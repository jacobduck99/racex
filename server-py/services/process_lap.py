from services.corner_detection import CornerDetector 

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
    print("heres' your corners", corner.corners)
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
    print("here's brake zones", brake.brake_zones)
    return brake.brake_zones





