from dataclasses import dataclass
from typing import Optional
from services.utils import convert_to_kph
from data_processing.corner import Corner 

class CornerDetection:
    def __init__(self): 
        self.car_rotating = False
        self.corners = []
        self.previous_corner = None
        self.merged_corners = []

    def open_corner(self, pct, t, yaw_rate):
        if not self.car_rotating:
            self.car_rotating = True
            self.rotating_pct = pct
            self.rotating_t = t
            self.yaw_rate = yaw_rate

    def close_corner(self, pct, t, yaw_rate):
        if self.car_rotating:
            self.car_rotating = False
            self.rotation_ended_pct = pct
            self.rotation_ended_t = t
            self.yaw_rate = yaw_rate
            completed_corner = Corner(self.rotating_pct, self.rotating_t, self.rotation_ended_pct, self.rotation_ended_t, yaw_rate=self.yaw_rate)
            self.corners.append(completed_corner) 
            self.yaw_rate = None

    def filter_corners(self, corners):
        clean_corners = []
        for corner in corners:
            corner_duration_pct = corner.rotation_ended_pct - corner.rotating_pct
            if corner_duration_pct > 0.004:  
                clean_corners.append(corner)
        return clean_corners

    def merge_corner(self, corners):
        for current_corner in corners:
            if self.previous_corner is None:
                self.previous_corner = current_corner
            else:
                gap_start = self.previous_corner.rotation_ended_pct
                gap_end = current_corner.rotating_pct
                gap = gap_end - gap_start

                if self.previous_corner.yaw_rate * current_corner.yaw_rate < 0:
                    self.merged_corners.append(self.previous_corner)
                    self.previous_corner = current_corner
                elif gap < 0.05:
                    self.previous_corner.rotation_ended_t = current_corner.rotation_ended_t
                    self.previous_corner.rotation_ended_pct = current_corner.rotation_ended_pct
                else:
                    self.merged_corners.append(self.previous_corner)
                    self.previous_corner = current_corner
        self.merged_corners.append(self.previous_corner)
        return self.merged_corners




