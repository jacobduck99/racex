
def brake_coaching(corners):
    brake_tips = []
    for matched_corners in corners:
        if matched_corners.fast.brake_zone is not None and matched_corners.ref.brake_zone is not None:
            distance = (matched_corners.fast.brake_zone.brake_on_pct - matched_corners.ref.brake_zone.brake_on_pct) * 100
            if matched_corners.fast.brake_zone.brake_on_pct > matched_corners.ref.brake_zone.brake_on_pct:
                tip = {
                    "braking" : "fast lap is braking later"
                }
                brake_tips.append(tip)
            elif matched_corners.fast.brake_zone.brake_on_pct < matched_corners.ref.brake_zone.brake_on_pct:
                tip = {
                    "braking" : "ref lap is braking later"
                }
                brake_tips.append(tip)
                print("brake_tips", brake_tips)
        else:
            continue 
            

