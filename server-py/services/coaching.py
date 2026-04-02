from services.utils import convert_to_meters

def brake_marker_coaching(corners, lap_dist):
    brake_tips = []
    for brake_zones in corners:
        
        fast_brake_zone = brake_zones.fast.brake_zone
        ref_brake_zone = brake_zones.ref.brake_zone

        if fast_brake_zone is not None and ref_brake_zone is not None:
            if fast_brake_zone.brake_on_pct == ref_brake_zone.brake_on_pct:
                brake_marker_same = {"braking": f"You are braking the same as your fastest lap sector {brake_zones.corner_num}"}
                brake_tips.append(brake_marker_same)
                continue

            decide_tip = "later" if fast_brake_zone.brake_on_pct > ref_brake_zone.brake_on_pct else "earlier"
            distance = abs(fast_brake_zone.brake_on_pct - ref_brake_zone.brake_on_pct)

            meters = int(convert_to_meters(lap_dist, distance))
            tips = {"braking" : f"You are braking {meters} meters {decide_tip} compared to your fastest laps sector {brake_zones.corner_num} brake marker"}

            brake_tips.append(tips)
    print("brake_tips", brake_tips)
    return brake_tips
            

