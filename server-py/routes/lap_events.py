
def find_brake_zone(lap):
    brake = False
    braking = []
    brake_release = []
    threshold = 0.01
    for sample in lap:
        if not brake and sample["brake"] >= threshold:
            braking.append(sample)
            brake = True
        elif brake == True and sample["brake"] < threshold: 
            brake_release.append(sample)
            brake = False
    return braking, brake_release
            
