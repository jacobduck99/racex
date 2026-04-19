import math

def convert_to_kph(speed):
    speed_in_kph = speed * 3.6
    return speed_in_kph

def get_lap_dist(samples):
    return max(sample["lapDist"] for sample in samples)

def convert_to_meters(lap_dist, distance):
    meters = lap_dist * distance
    return meters

def create_track_map(samples):
    coordinates = []
    for k in samples:
        matched = { "lon": k["lon"], "lat": k["lat"]}
        coordinates.append(matched) 
    return coordinates

def add_sectors_track_map(sectors, trackmap):
    for t in trackmap:
        for s in sectors:
            if math.isclose(s.start_sector_lon, t["lon"]) and math.isclose(s.start_sector_lat, t["lat"]):
                t["sector_start_lon"] = s.start_sector_lon
                t["sector_start_lat"] = s.start_sector_lat
            if math.isclose(s.end_sector_lon, t["lon"]) and math.isclose(s.end_sector_lat, t["lat"]):
                t["sector_end_lon"] = s.end_sector_lon
                t["sector_end_lat"] = s.end_sector_lat
    print(trackmap)

    
