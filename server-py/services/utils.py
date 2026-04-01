
def convert_to_kph(speed):
    speed_in_kph = speed * 3.6
    return speed_in_kph

def get_lap_dist(samples):
    track_length = []
    track_dist = []
    for sample in samples:
        track_dist.append(sample["lapDist"])
        track_length = max(track_dist)
    print("here's track_length", track_length)
    return track_length

def convert_to_meters(lap_dist, distance):
    meters = lap_dist * distance
    return meters

    
