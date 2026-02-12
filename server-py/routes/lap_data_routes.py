from flask import Blueprint, request, jsonify
import json
from routes.lap_events import find_brake_zone

analyse_bp = Blueprint("analyse", __name__)

@analyse_bp.route("/lap-data/analyse", methods=["POST"])
def analyse_lap_upload():
    data = request.get_json()

    if not isinstance(data, dict):
        return jsonify({"error": "Expected JSON object"}), 400

    laps = data.get("laps")
    if not isinstance(laps, list):
        return jsonify({"error": "Expected 'laps' to be a list"}), 400

    lap_objects = []
    for lap in laps:
        lap_objects.append(lap)

    sorted_laps = sorted(lap_objects, key=lambda lap: lap.get("lapTime", float("inf")))

    fastest_lap = sorted_laps[0] if sorted_laps else None
    second_fastest_lap = sorted_laps[1] if sorted_laps else None
    fastest_samples = fastest_lap.get("samples", []) if fastest_lap else []
    second_fastest_samples = second_fastest_lap.get("samples", []) if second_fastest_lap else []

    fast_lap_brake_zone = find_brake_zone(fastest_samples) 
    fast_duration_s = fast_lap_brake_zone["duration_s"]
    fast_zone_pct = fast_lap_brake_zone["zone_pct"]
    print("here's your braking duration fastest lap", fast_duration_s)
    print("here's your braking zone pct fast lap", fast_zone_pct)

    second_fastest_lap_brake_zone = find_brake_zone(second_fastest_samples)
    
    print("here's your braking zone second fastest lap", second_fastest_lap_brake_zone)

    # print("here's your fastest lap samples for t1 \n", fast_lap_braking)

    # print("here's your second fast lap samples for t1 \n", second_fast_lap_braking)

    # print("fastest lapTime:", fastest_lap.get("lapTime") if fastest_lap else None)
    # print("fastest samples count:", len(fastest_samples))

    # print("second fastest lapTime:", second_fastest_lap.get("lapTime") if second_fastest_lap else None)
    # print("second fastest sample count:", len(second_fastest_samples))

    return jsonify({
        "laps": len(laps),
        "fastestLapTime": fastest_lap.get("lapTime") if fastest_lap else None,
        "fastestLapSamples": len(fastest_samples),
    })
