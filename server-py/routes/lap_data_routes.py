from flask import Blueprint, request, jsonify
import json
from routes.lap_events import find_brake_zones

analyse_bp = Blueprint("analyse", __name__)

@analyse_bp.route("/lap-data/analyse", methods=["POST"])
def analyse_lap_upload():
    data = request.get_json()

    if not isinstance(data, dict):
        return jsonify({"error": "Expected JSON object"}), 400

    laps = data.get("laps")
    if not isinstance(laps, list):
        return jsonify({"error": "Expected 'laps' to be a list"}), 400

    if len(laps) <= 1:
        return jsonify({"error": "Expected at least 2 laps to compare"}), 400

    sorted_laps = sorted(laps, key=lambda lap: lap.get("lapTime", float("inf")))
    fastest_lap = sorted_laps[0] if sorted_laps else None
    second_fastest_lap = sorted_laps[1]

    fastest_samples = fastest_lap.get("samples", []) if fastest_lap else []
    second_fastest_samples = second_fastest_lap.get("samples", []) if second_fastest_lap else []

    fast = find_brake_zones(fastest_samples)
    second = find_brake_zones(second_fastest_samples)

    fast_corners = fast.get("corners", [])
    second_corners = second.get("corners", [])

    fast_first = fast_corners[0] if fast_corners else None
    second_first = second_corners[0] if second_corners else None

    if not fast_first or not second_first:
        return jsonify({
            "error": "Could not detect a brake zone in one of the laps (try lowering threshold or ensure brake data exists)."
        }), 400

    fast_duration_s = fast_first["duration_s"]
    fast_brake_on_pct = fast_first["brake_on_pct"]
    fast_brake_off_pct = fast_first["brake_off_pct"]
    fast_zone_pct = fast_first["zone_pct"]
    fast_lap_min_speed = fast_first["min_speed"]
    fast_min_speed_pct = fast_first["min_speed_pct"]

    second_duration_s = second_first["duration_s"]
    second_brake_on_pct = second_first["brake_on_pct"]
    second_brake_off_pct = second_first["brake_off_pct"]
    second_zone_pct = second_first["zone_pct"]
    second_lap_min_speed = second_first["min_speed"]
    second_min_speed_pct = second_first["min_speed_pct"]

    compare_min_speeds = fast_lap_min_speed - second_lap_min_speed

    result = {
        "fastest_lap": {
            "corner_num": fast_first["corner_num"],
            "duration_s": fast_duration_s,
            "brake_on_pct": fast_brake_on_pct,
            "brake_off_pct": fast_brake_off_pct,
            "zone_pct": fast_zone_pct,
            "min_speed": fast_lap_min_speed,
            "min_speed_pct": fast_min_speed_pct,
            "steering_samples_count": len(fast_first.get("steering_samples", [])),
        },
        "second_fastest_lap": {
            "corner_num": second_first["corner_num"],
            "duration_s": second_duration_s,
            "brake_on_pct": second_brake_on_pct,
            "brake_off_pct": second_brake_off_pct,
            "zone_pct": second_zone_pct,
            "min_speed": second_lap_min_speed,
            "min_speed_pct": second_min_speed_pct,
            "steering_samples_count": len(second_first.get("steering_samples", [])),
        },
        "comparison": {
            "min_speed_delta": compare_min_speeds,
            "min_speed_delta_kph": compare_min_speeds * 3.6,
            "duration_delta_s": fast_duration_s - second_duration_s,
            "zone_pct_delta": fast_zone_pct - second_zone_pct,
        },
    }

    return jsonify({"result": result})
