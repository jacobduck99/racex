from flask import Blueprint, request, jsonify
import json
from routes.lap_events import find_brake_zones, find_corners_by_yaw_rate, build_corner_map, match_zones, match_braking_to_corners

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
    fast_lap_corner_matched = match_braking_to_corners(fastest_samples)
    print("here's returned matched corners", json.dumps(fast_lap_corner_matched, indent=2))
    reference_lap_corner_map = build_corner_map(reference_samples)
    matched_zones = match_zones(fast_lap_corner_map, reference_lap_corner_map)

    return jsonify({"matched_zones": matched_zones})
                    
