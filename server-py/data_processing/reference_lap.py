from collections import defaultdict

from data_processing.process_lap import analyse_lap
from data_processing.corner import Corner
from data_processing.brake_detection import Brake
from data_processing.throttle_detection import Throttle
from services.utils import get_median

def build_reference_lap(reference_laps, track_corners=None):
    reference_samples = []
    corners_by_position = defaultdict(list)
    for i, lap in enumerate(reference_laps, 1):
        samples = lap["samples"]
        corners = analyse_lap(samples, track_corners)
        reference_samples.append({"lap": i, "corners": corners})
    for c in reference_samples:
        for i, r in enumerate(c["corners"], start=1):
            corners_by_position[i].append(r)
    return corners_by_position

def build_median_reference_corners(corners_by_position):
    return [
        _median_corner(corners_by_position[corner_num])
        for corner_num in sorted(corners_by_position)
    ]

def _median_corner(corners):
    min_speeds = [c.min_speed for c in corners if c.min_speed is not None]
    gears = [c.gear for c in corners if c.gear is not None]

    return Corner(
        rotating_pct=get_median([c.rotating_pct for c in corners]),
        rotating_t=get_median([c.rotating_t for c in corners]),
        rotation_ended_pct=get_median([c.rotation_ended_pct for c in corners]),
        rotation_ended_t=get_median([c.rotation_ended_t for c in corners]),
        start_sector_lon=get_median([c.start_sector_lon for c in corners]),
        start_sector_lat=get_median([c.start_sector_lat for c in corners]),
        end_sector_lon=get_median([c.end_sector_lon for c in corners]),
        end_sector_lat=get_median([c.end_sector_lat for c in corners]),
        brake_zone=_median_brake_zone([c.brake_zone for c in corners if c.brake_zone]),
        throttle=_median_throttle([c.throttle for c in corners if c.throttle]),
        min_speed=get_median(min_speeds) if min_speeds else None,
        gear=round(get_median(gears)) if gears else None,
    )

def _median_brake_zone(brake_zones):
    if not brake_zones:
        return None
    return Brake(
        brake_on_pct=get_median([b.brake_on_pct for b in brake_zones]),
        brake_on_t=get_median([b.brake_on_t for b in brake_zones]),
        brake_off_pct=get_median([b.brake_off_pct for b in brake_zones]),
        brake_off_t=get_median([b.brake_off_t for b in brake_zones]),
        max_brake_pressure=get_median([b.max_brake_pressure for b in brake_zones]),
    )

def _median_throttle(throttles):
    if not throttles:
        return None
    return Throttle(
        throttle_off_pct=get_median([t.throttle_off_pct for t in throttles]),
        throttle_off_t=get_median([t.throttle_off_t for t in throttles]),
        throttle_on_pct=get_median([t.throttle_on_pct for t in throttles]),
        throttle_on_t=get_median([t.throttle_on_t for t in throttles]),
    )
