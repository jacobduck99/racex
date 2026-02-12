#pct means distance around track 

def find_brake_zone(lap):
    brake = False
    brake_on_pct = None
    brake_on_t = None
    brake_off_pct = None
    brake_off_t = None
    threshold = 0.05
    for sample in lap:
        if not brake and sample["brake"] >= threshold:
            brake_on_pct = sample["pct"]
            brake_on_t = sample["t"]
            brake = True
        elif brake == True and sample["brake"] < threshold: 
            brake_off_pct = sample["pct"]
            brake_off_t = sample["t"]
            brake = False
            break
    duration_s = brake_off_t - brake_on_t
    zone_pct = brake_off_pct - brake_on_pct
    return { "duration_s": duration_s, "zone_pct": zone_pct} 
            
