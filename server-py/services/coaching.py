from services.utils import convert_to_meters

def brake_marker_coaching(corners, lap_dist):
    coaching = []
    for brake_zones in corners:
        
        fast_brake_zone = brake_zones.fast.brake_zone
        ref_brake_zone = brake_zones.ref.brake_zone

        if fast_brake_zone is not None and ref_brake_zone is not None:
            if fast_brake_zone.brake_on_pct == ref_brake_zone.brake_on_pct:

                brake_marker_same = {"braking": f"You are braking the same as your fastest lap sector {brake_zones.corner_num}"}
                coaching.append(brake_marker_same)
                continue

            decide_tip = "later" if fast_brake_zone.brake_on_pct > ref_brake_zone.brake_on_pct else "earlier"
            distance = abs(fast_brake_zone.brake_on_pct - ref_brake_zone.brake_on_pct)

            meters = int(convert_to_meters(lap_dist, distance))
            check_meters = "meter" if meters == 1 else "meters"

            tips = {"Sector": brake_zones.corner_num, "braking" : f"You are braking {meters} {check_meters} {decide_tip} compared to your fastest laps sector {brake_zones.corner_num} brake marker"}

            coaching.append(tips)
    print("brake_tips", coaching)
    return coaching
            

