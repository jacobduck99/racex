from flask import Blueprint, request, jsonify
import json

from data_processing.process_lap import analyse_lap
from data_processing.matching import match_zones

from services.coaching import coaching

from services.utils import get_lap_dist, create_track_map, add_sectors_track_map

analyse_bp = Blueprint("analyse", __name__)

@analyse_bp.route("/lap-data/analyse", methods=["POST"])
def analyse_lap_upload():
    data = request.get_json()
    if not isinstance(data, dict):
        return jsonify({"error": "Expected JSON object"}), 400

    laps = data.get("cleaned")
    for i in range(len(laps)):
        print("laps", i)

    if not isinstance(laps, list):
        return jsonify({"error": "Expected 'laps' to be a list"}), 400

    if len(laps) <= 1:
        return jsonify({"error": "Expected at least 2 clean laps to compare"}), 400

    sorted_laps = sorted(laps, key=lambda lap: lap.get("lapTime", float("inf")))
    fastest_lap = sorted_laps[0] if sorted_laps else None
    reference_lap = sorted_laps[1]
    rest_of_laps = sorted_laps[2:]
    for i, lap in enumerate(rest_of_laps, start=3):
        print(f"lap rank {i}, time {lap.get('lapTime')}")

    fastest_samples = fastest_lap.get("samples", []) if fastest_lap else []
    track_map = create_track_map(fastest_samples)
    lap_dist = get_lap_dist(fastest_samples)
    reference_samples = reference_lap.get("samples", []) if reference_lap else []

    fast_matched_corners = analyse_lap(fastest_samples) 

    reference_matched_corners = analyse_lap(reference_samples)

    matched_corners = match_zones(fast_matched_corners, reference_matched_corners) 
    track_map_and_sectors = add_sectors_track_map(
        [m.fast for m in matched_corners],
        track_map,
    )
    coach = coaching(matched_corners, lap_dist)

    return jsonify({"coaching": coach, "track_map": track_map_and_sectors })
                    
