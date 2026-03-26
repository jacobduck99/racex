from flask import Blueprint, request, jsonify
import json

from services.process_lap import analyse_lap, match_zones

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
    matched_zones = match_zones(matched_corners1, matched_corners2)

    return jsonify({"matched_zones": matched_zones})
                    
