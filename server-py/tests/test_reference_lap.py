from data_processing.reference_lap import build_median_reference_corners
from data_processing.corner import Corner
from data_processing.brake_detection import Brake
from data_processing.throttle_detection import Throttle


def make_corner(brake_on_pct, throttle_on_pct, gear, min_speed, max_brake_pressure=0.8):
    return Corner(
        rotating_pct=0.35,
        rotating_t=3.5,
        rotation_ended_pct=0.45,
        rotation_ended_t=4.5,
        start_sector_lon=0,
        start_sector_lat=0,
        end_sector_lon=0,
        end_sector_lat=0,
        brake_zone=Brake(
            brake_on_pct=brake_on_pct,
            brake_on_t=brake_on_pct * 10,
            brake_off_pct=0.37,
            brake_off_t=3.7,
            max_brake_pressure=max_brake_pressure,
        ),
        min_speed=min_speed,
        throttle=Throttle(
            throttle_off_pct=throttle_on_pct - 0.001,
            throttle_off_t=(throttle_on_pct - 0.001) * 10,
            throttle_on_pct=throttle_on_pct,
            throttle_on_t=throttle_on_pct * 10,
        ),
        gear=gear,
    )


def test_median_reference_corner_uses_median_not_any_single_lap():
    # Three reference laps for the SAME corner (position 1), each braking/
    # throttling at a different point, in a different gear, at a different
    # min speed — deliberately spread so the median is obviously distinct
    # from every individual lap's own value.
    lap_a = make_corner(brake_on_pct=0.28, throttle_on_pct=0.36, gear=3, min_speed=72, max_brake_pressure=0.75)
    lap_b = make_corner(brake_on_pct=0.31, throttle_on_pct=0.39, gear=4, min_speed=68, max_brake_pressure=0.80)
    lap_c = make_corner(brake_on_pct=0.33, throttle_on_pct=0.40, gear=4, min_speed=65, max_brake_pressure=0.90)

    corners_by_position = {1: [lap_a, lap_b, lap_c]}

    result = build_median_reference_corners(corners_by_position)

    assert len(result) == 1
    median_corner = result[0]

    assert median_corner.brake_zone.brake_on_pct == 0.31
    assert median_corner.brake_zone.max_brake_pressure == 0.80
    assert median_corner.throttle.throttle_on_pct == 0.39
    assert median_corner.gear == 4
    assert median_corner.min_speed == 68

    # None of these values are just "the first reference lap" or "the last
    # reference lap" — they're genuinely the median of all three.
    assert median_corner.brake_zone.brake_on_pct not in (lap_a.brake_zone.brake_on_pct,)
    assert median_corner.min_speed != lap_a.min_speed


def test_median_reference_corner_ignores_laps_missing_data_for_that_corner():
    lap_a = make_corner(brake_on_pct=0.28, throttle_on_pct=0.36, gear=3, min_speed=72)
    lap_b = make_corner(brake_on_pct=0.31, throttle_on_pct=0.39, gear=4, min_speed=68)
    lap_c = Corner(
        rotating_pct=0.35,
        rotating_t=3.5,
        rotation_ended_pct=0.45,
        rotation_ended_t=4.5,
        start_sector_lon=0,
        start_sector_lat=0,
        end_sector_lon=0,
        end_sector_lat=0,
        # no braking/throttle/gear detected for this corner on this lap
        brake_zone=None,
        min_speed=None,
        throttle=None,
        gear=None,
    )

    corners_by_position = {1: [lap_a, lap_b, lap_c]}

    result = build_median_reference_corners(corners_by_position)[0]

    # median of just [0.28, 0.31] since lap_c contributed nothing
    assert result.brake_zone.brake_on_pct == (0.28 + 0.31) / 2
    assert result.gear in (3, 4)
    assert result.min_speed == (72 + 68) / 2
