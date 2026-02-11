#pct means distance around track 

def find_brake_zone(lap):
    brake = False
    brake_on_pct = None
    brake_off_pct = None
    threshold = 0.05
    for sample in lap:
        if not brake and sample["brake"] >= threshold:
            brake_on_pct = sample["pct"]
            brake = True
        elif brake == True and sample["brake"] < threshold: 
            brake_off_pct = sample["pct"]
            brake = False
            break
    brake_dist = brake_off_pct - brake_on_pct
    return brake_dist
            
