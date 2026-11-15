from dataclasses import dataclass
from typing import Optional
from services.utils import convert_to_kph
from data_processing.corner import Corner

# All distances below are fractions of a lap (LapDistPct: 0.0 = start line, 1.0 = full lap).

# A detected corner within this distance of a known track corner counts as that corner.
TRACK_CORNER_MATCH_PCT = 0.01
# Corners shorter than this are noise (a twitch of the wheel), not a real corner.
MIN_CORNER_LENGTH_PCT = 0.004
# Merged corners can't grow longer than this, so a sequence of bends isn't merged into one.
MAX_MERGED_CORNER_PCT = 0.06
# Two same-direction rotations closer than this are treated as one corner.
MERGE_GAP_PCT = 0.01

class CornerDetection:
    def __init__(self):
        self.car_rotating = False
        self.corners = []

    def open_corner(self, pct, t, yaw_rate, lon, lat):
        if not self.car_rotating:
            self.car_rotating = True
            self.rotating_pct = pct
            self.rotating_t = t
            self.yaw_rate = yaw_rate
            self.start_sector_lon = lon
            self.start_sector_lat = lat

    def close_corner(self, pct, t, yaw_rate, lon, lat):
        if self.car_rotating:
            self.car_rotating = False
            self.rotation_ended_pct = pct
            self.rotation_ended_t = t
            self.yaw_rate = yaw_rate
            self.end_sector_lon = lon
            self.end_sector_lat = lat
            completed_corner = Corner(self.rotating_pct, self.rotating_t, self.rotation_ended_pct, self.rotation_ended_t, self.start_sector_lon, self.start_sector_lat, self.end_sector_lon, self.end_sector_lat, yaw_rate=self.yaw_rate)
            self.corners.append(completed_corner) 
            self.yaw_rate = None

    def filter_corners(self, corners, track_corners=None):
        clean_corners = []
        if track_corners is not None:
            for corner in corners:
                for track_corner in track_corners:
                    if abs(corner.rotating_pct - track_corner.rotating_pct) <= TRACK_CORNER_MATCH_PCT:
                        clean_corners.append(corner)
                        break
        else:
            for corner in corners:
                corner_duration_pct = corner.rotation_ended_pct - corner.rotating_pct
                if corner_duration_pct > MIN_CORNER_LENGTH_PCT:
                    clean_corners.append(corner)
        return clean_corners

    def merge_corner(self, corners):
        # local variables (not self.*) so calling this twice doesn't mix results
        merged_corners = []
        reference_corner = None
        for current_corner in corners:
            if reference_corner is None:
                reference_corner = current_corner
                continue

            gap = current_corner.rotating_pct - reference_corner.rotation_ended_pct
            corner_dist = current_corner.rotation_ended_pct - reference_corner.rotating_pct
            changes_direction = reference_corner.yaw_rate * current_corner.yaw_rate < 0

            if not changes_direction and corner_dist <= MAX_MERGED_CORNER_PCT and gap < MERGE_GAP_PCT:
                # same corner: extend the reference corner to where this one ends
                reference_corner.rotation_ended_t = current_corner.rotation_ended_t
                reference_corner.rotation_ended_pct = current_corner.rotation_ended_pct
                reference_corner.end_sector_lon = current_corner.end_sector_lon
                reference_corner.end_sector_lat = current_corner.end_sector_lat
            else:
                merged_corners.append(reference_corner)
                reference_corner = current_corner

        if reference_corner is not None:
            merged_corners.append(reference_corner)
        return merged_corners
