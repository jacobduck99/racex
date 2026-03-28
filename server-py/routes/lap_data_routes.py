from flask import Blueprint, request, jsonify
import json

from data_processing.process_lap import analyse_lap, match_zones

from services.coaching import brake_coaching

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

    fast_matched_corners = analyse_lap(fastest_samples) 
    reference_matched_corners = analyse_lap(reference_samples)
    matched_corners = match_zones(fast_matched_corners, reference_matched_corners) 
    for corners in matched_corners:
        print("here's your ref rotating", corners.ref.rotating_pct)
        print("here's your ref rotating end", corners.ref.rotation_ended_pct)
        print("here's your fast rotating", corners.fast.rotating_pct)
        print("here's your fast rotating_ended", corners.fast.rotation_ended_pct)

    return jsonify({"matched_zones": matched_corners})
                    
