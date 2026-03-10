from flask import Blueprint, request, jsonify
import json
from routes.lap_events import find_brake_zones, find_corners_by_yaw_rate, build_corner_map

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
    reference_lap = sorted_laps[1]

    fastest_samples = fastest_lap.get("samples", []) if fastest_lap else []
    reference_samples = reference_lap.get("samples", []) if reference_lap else []
    
    fast_lap_corner_map = build_corner_map(fastest_samples)
    reference_lap_corner_map = build_corner_map(second_fastest_sample)
    print("here's whats in corner map \n", json.dumps(corner_map, indent=2))
    

    # i already do this now fast = find_brake_zones(fastest_samples)
    # i already do this now second = find_brake_zones(second_fastest_samples)
    # was returning first index for now

    #fast_corners = fast.get("corners", [])

    #second_corners = second.get("corners", []) 

    #fast_first = fast_corners[0] if fast_corners else None
    #second_first = second_corners[0] if second_corners else None

    #if not fast_first or not second_first:
    #    return jsonify({
    #        "error": "Could not detect a brake zone in one of the laps (try lowering threshold or ensure brake data exists)."
    #    }), 400

# NEED TO CONVERT THIS INTO A FUNCTION AND LOOP THROUGH ALL OF MAX SPEED
#    max_speed_kph = fast_first["max_speed"] * 3.6
#    max_speed_rounded = int(round(max_speed_kph))

#    second_max_speed_kph = second_first["max_speed"] * 3.6
#    second_max_speed_rounded = int(round(second_max_speed_kph))
 
# probably delete    compare_min_speeds = fast_first["min_speed"] - second_first["min_speed"] 

    result = {
        "fastest_lap": {
            "corner_num": fast_first["corner_num"],
            "duration_s": fast_first["duration_s"],
            "brake_on_pct": fast_first["brake_on_pct"],
            "brake_off_pct": fast_first["brake_off_pct"],
            "zone_pct": fast_first["zone_pct"],
            "min_speed": fast_first["min_speed"],
            "min_speed_pct": fast_first["min_speed_pct"],
            "steering_samples_count": len(fast_first.get("steering_samples", [])),
            "max_brake": fast_first["max_brake"],
            "max_brake_pct": fast_first["max_brake_pct"],
            "max_speed_kph": max_speed_rounded,
            "coasting": fast_first["coast_duration_s"] 
        },
        "second_fastest_lap": {
            "corner_num": second_first["corner_num"],
            "duration_s": second_first["duration_s"],
            "brake_on_pct": second_first["brake_on_pct"],
            "brake_off_pct": second_first["brake_off_pct"],
            "zone_pct": second_first["zone_pct"],
            "min_speed": second_first["min_speed"],
            "min_speed_pct": second_first["min_speed_pct"],
            "steering_samples_count": len(second_first.get("steering_samples", [])),
            "max_brake": second_first["max_brake"],
            "max_brake_pct": second_first["max_brake_pct"],
            "max_speed_kph": second_max_speed_rounded,
            "coasting": second_first["coast_duration_s"]
        },
        "comparison": {
            "min_speed_delta": compare_min_speeds,
            "min_speed_delta_kph": compare_min_speeds * 3.6,
            "duration_delta_s": fast_first["duration_s"] - second_first["duration_s"],
            "zone_pct_delta": fast_first["zone_pct"] - second_first["zone_pct"],
        },
    }

    return jsonify({"result": result})
