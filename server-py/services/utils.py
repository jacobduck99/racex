
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
    track_and_sectors = []
    for t in trackmap:
        for s in sectors:

            start_sector_lon = s.start_sector_lon
            start_sector_lat = s.start_sector_lat
            end_sector_lon = s.end_sector_lon
            end_sector_lat = s.end_sector_lat

            if start_sector_lon and start_sector_lat == t["lon"] and t["lat"]:
                sector = { "start_sector_lon": start_sector_lon, start_sector_lat: start_sector_lat, "track_lon": t["lon"], "track_lat": t["lat"]}
                track_and_sectors.append(sector)
    print("here's sectors on track", track_and_sectors)



    
