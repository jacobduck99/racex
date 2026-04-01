from services.utils import convert_to_meters

def brake_marker_coaching(corners, lap_dist):
    brake_tips = []
    for brake_zones in corners:
        
        fast_brake_zone = brake_zones.fast.brake_zone
        ref_brake_zone = brake_zones.ref.brake_zone

        if fast_brake_zone is not None and ref_brake_zone is not None:
            check_tip = "later" if fast_brake_zone.brake_on_pct > ref_brake_zone.brake_on_pct else "earlier"
            distance = abs(fast_brake_zone.brake_on_pct - ref_brake_zone.brake_on_pct)
            meters = int(convert_to_meters(lap_dist, distance))
            tip = {"Sector": brake_zones.corner_num ,"braking" : f"Ref is braking {meters} meters {check_tip}"}

            brake_tips.append(tip)
    print("brake_tips", brake_tips)
    return brake_tips
            

