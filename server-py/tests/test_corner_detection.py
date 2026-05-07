
from data_processing.corner_detection import CornerDetection
from data_processing.corner import Corner

def test_filter_corners_keeps_only_corners_above_threshold():
    detector = CornerDetection()
    test_corners = [
    Corner(rotating_pct=0.001, rotating_t=0, rotation_ended_pct=0.004, rotation_ended_t=0,
           start_sector_lon=0, start_sector_lat=0, end_sector_lon=0, end_sector_lat=0,
           brake_zone=None, min_speed=None, throttle=None, yaw_rate=0.1, gear=None),
    Corner(rotating_pct=0.002, rotating_t=0, rotation_ended_pct=0.005, rotation_ended_t=0,
           start_sector_lon=0, start_sector_lat=0, end_sector_lon=0, end_sector_lat=0,
           brake_zone=None, min_speed=None, throttle=None, yaw_rate=0.1, gear=None),
    Corner(rotating_pct=0.001, rotating_t=0, rotation_ended_pct=0.006, rotation_ended_t=0,
           start_sector_lon=0, start_sector_lat=0, end_sector_lon=0, end_sector_lat=0,
           brake_zone=None, min_speed=None, throttle=None, yaw_rate=0.1, gear=None),
    Corner(rotating_pct=0.001, rotating_t=0, rotation_ended_pct=0.007, rotation_ended_t=0,
           start_sector_lon=0, start_sector_lat=0, end_sector_lon=0, end_sector_lat=0,
           brake_zone=None, min_speed=None, throttle=None, yaw_rate=0.1, gear=None),
    Corner(rotating_pct=0.000, rotating_t=0, rotation_ended_pct=0.010, rotation_ended_t=0,
           start_sector_lon=0, start_sector_lat=0, end_sector_lon=0, end_sector_lat=0,
           brake_zone=None, min_speed=None, throttle=None, yaw_rate=0.1, gear=None),
]
    result = detector.filter_corners(test_corners)
    assert result == [test_corners[2], test_corners[3], test_corners[4]]

def test_merge_corners_less_than_threshold_same_yawrate_sign():
    detector = CornerDetection()
    test_corners = [
    Corner(rotating_pct=0.001, rotating_t=0, rotation_ended_pct=0.004, rotation_ended_t=0,
           start_sector_lon=0, start_sector_lat=0, end_sector_lon=0, end_sector_lat=0,
           brake_zone=None, min_speed=None, throttle=None, yaw_rate=0.1, gear=None),

    Corner(rotating_pct=0.005, rotating_t=0, rotation_ended_pct=0.008, rotation_ended_t=0,
           start_sector_lon=0, start_sector_lat=0, end_sector_lon=0, end_sector_lat=0,
           brake_zone=None, min_speed=None, throttle=None, yaw_rate=0.1, gear=None),
]
    result = detector.merge_corner(test_corners)
    assert result[0].rotation_ended_pct == 0.008

def test_merge_corner_diff_yaw_rate():
    detector = CornerDetection()
    test_corners = [
    Corner(rotating_pct=0.001, rotating_t=0, rotation_ended_pct=0.004, rotation_ended_t=0,
           start_sector_lon=0, start_sector_lat=0, end_sector_lon=0, end_sector_lat=0,
           brake_zone=None, min_speed=None, throttle=None, yaw_rate=-0.1, gear=None),

    Corner(rotating_pct=0.005, rotating_t=0, rotation_ended_pct=0.008, rotation_ended_t=0,
           start_sector_lon=0, start_sector_lat=0, end_sector_lon=0, end_sector_lat=0,
           brake_zone=None, min_speed=None, throttle=None, yaw_rate=0.1, gear=None),
]
    result = detector.merge_corner(test_corners)
    assert result == [test_corners[0], test_corners[1]]

def test_merge_corner_dist():
    detector = CornerDetection()
    test_corners = [
    Corner(rotating_pct=0.001, rotating_t=0, rotation_ended_pct=0.004, rotation_ended_t=0,
           start_sector_lon=0, start_sector_lat=0, end_sector_lon=0, end_sector_lat=0,
           brake_zone=None, min_speed=None, throttle=None, yaw_rate=0.1, gear=None),

    Corner(rotating_pct=0.140, rotating_t=0, rotation_ended_pct=0.148, rotation_ended_t=0,
           start_sector_lon=0, start_sector_lat=0, end_sector_lon=0, end_sector_lat=0,
           brake_zone=None, min_speed=None, throttle=None, yaw_rate=0.1, gear=None),
]
    result = detector.merge_corner(test_corners)
    assert result == [test_corners[0], test_corners[1]]













