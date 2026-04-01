
def brake_marker_coaching(corners):
    brake_tips = []
    for brake_zones in corners:
        
        fast_brake_zone = brake_zones.fast.brake_zone
        ref_brake_zone = brake_zones.ref.brake_zone

        if fast_brake_zone is not None and ref_brake_zone is not None:
            check_tip = "later" if fast_brake_zone.brake_on_pct > ref_brake_zone.brake_on_pct else "earlier"
            distance = abs(fast_brake_zone.brake_on_pct - ref_brake_zone.brake_on_pct) * 100

            tip = {"Sector": brake_zones.corner_num ,"braking" : f"Ref is braking {distance} {check_tip}"}

            brake_tips.append(tip)
    print("brake_tips", brake_tips)
    return brake_tips
            

