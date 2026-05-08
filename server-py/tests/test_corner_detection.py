from data_processing.corner_detection import CornerDetection
from data_processing.corner import Corner
import pytest

@pytest.fixture
def detector():
    return CornerDetection()

def make_corner(rotating_pct=0, rotation_ended_pct=0, yaw_rate=0.1, **kwargs):
    return Corner(
        rotating_pct=rotating_pct,
        rotating_t=kwargs.get("rotating_t", 0),
        rotation_ended_pct=rotation_ended_pct,
        rotation_ended_t=kwargs.get("rotation_ended_t", 0),
        start_sector_lon=kwargs.get("start_sector_lon", 0),
        start_sector_lat=kwargs.get("start_sector_lat", 0),
        end_sector_lon=kwargs.get("end_sector_lon", 0),
        end_sector_lat=kwargs.get("end_sector_lat", 0),
        brake_zone=kwargs.get("brake_zone", None),
        min_speed=kwargs.get("min_speed", None),
        throttle=kwargs.get("throttle", None),
        yaw_rate=yaw_rate,
        gear=kwargs.get("gear", None),
    )

def test_keeps_only_corners_above_threshold(detector):
    corners = [
        make_corner(rotating_pct=0.001, rotation_ended_pct=0.004),
        make_corner(rotating_pct=0.002, rotation_ended_pct=0.005),
        make_corner(rotating_pct=0.001, rotation_ended_pct=0.006),
        make_corner(rotating_pct=0.001, rotation_ended_pct=0.007),
        make_corner(rotating_pct=0.000, rotation_ended_pct=0.010),
    ]
    result = detector.filter_corners(corners)
    assert result == [corners[2], corners[3], corners[4]]

def test_matches_corners_to_track_corners(detector):
    corners = [
        make_corner(rotating_pct=0.05, rotation_ended_pct=0.08),
        make_corner(rotating_pct=0.15, rotation_ended_pct=0.18),
        make_corner(rotating_pct=0.30, rotation_ended_pct=0.33),
        make_corner(rotating_pct=0.45, rotation_ended_pct=0.48),
        make_corner(rotating_pct=0.60, rotation_ended_pct=0.63),
        make_corner(rotating_pct=0.90, rotation_ended_pct=0.93),
    ]
    track_corners = [
        make_corner(rotating_pct=0.05, rotation_ended_pct=0.08),
        make_corner(rotating_pct=0.15, rotation_ended_pct=0.18),
        make_corner(rotating_pct=0.30, rotation_ended_pct=0.33),
        make_corner(rotating_pct=0.45, rotation_ended_pct=0.48),
        make_corner(rotating_pct=0.60, rotation_ended_pct=0.63),
    ]
    result = detector.filter_corners(corners, track_corners)
    assert result == [corners[0], corners[1], corners[2], corners[3], corners[4]]

def test_same_yawrate_sign_less_than_threshold_merge_corners(detector):
    corners = [
        make_corner(rotating_pct=0.001, rotation_ended_pct=0.004),
        make_corner(rotating_pct=0.005, rotation_ended_pct=0.008),
    ]
    result = detector.merge_corner(corners)
    assert result[0].rotation_ended_pct == 0.008

def test_yaw_rate_flipped_dont_merge(detector):
    corners = [
        make_corner(rotating_pct=0.001, rotation_ended_pct=0.004, yaw_rate=-0.1),
        make_corner(rotating_pct=0.005, rotation_ended_pct=0.008, yaw_rate=0.1),
    ]
    result = detector.merge_corner(corners)
    assert result == [corners[0], corners[1]]

def test_dist_greater_than_threshold_dont_merge(detector):
    corners = [
        make_corner(rotating_pct=0.001, rotation_ended_pct=0.004),
        make_corner(rotating_pct=0.140, rotation_ended_pct=0.148),
    ]
    result = detector.merge_corner(corners)
    assert result == [corners[0], corners[1]]

def test_if_corner_dist_and_gap_dont_meet_threshold_and_same_yaw_rate_dont_merge(detector):
    corners = [
        make_corner(rotating_pct=0.100, rotation_ended_pct=0.140, yaw_rate=0.1),
        make_corner(rotating_pct=0.155, rotation_ended_pct=0.160, yaw_rate=0.1),
    ]
    result = detector.merge_corner(corners)
    assert result == [corners[0], corners[1]]























