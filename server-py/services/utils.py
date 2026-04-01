
def convert_to_kph(speed):
    speed_in_kph = speed * 3.6
    return speed_in_kph

def get_lap_dist(samples):
    track_length = []
    for sample in samples:
        if sample["lapDist"]:
            max_length = max(sample["lapDist"])
            track_length.append(max_length)
    print("track_length", track_length)
    return track_length

            

def conver_to_meters(lap_dist):
    pass
