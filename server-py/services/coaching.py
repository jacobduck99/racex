
def brake_coaching(corners):
    brake_tips = []
    for matched_corners in corners:
        if matched_corners.fast.brake_zone is not None and matched_corners.ref.brake_zone is not None:
            if matched_corners.fast.brake_zone.brake_on_pct > matched_corners.ref.brake_zone.brake_on_pct:
                tip = f"Fast lap is braking later, corner: {matched_corners.corner_num}"
                brake_tips.append(tip)
            print("brake_tips", brake_tips)
        else:
            continue 
            

