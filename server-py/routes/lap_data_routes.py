from flask import Blueprint, request, jsonify
import json

from data_processing.process_lap import analyse_lap
from data_processing.matching import match_zones
from data_processing.reference_lap import build_reference_lap

from services.coaching import coaching

from services.utils import get_lap_dist, create_track_map, add_sectors_track_map

analyse_bp = Blueprint("analyse", __name__)

@analyse_bp.route("/lap-data/analyse", methods=["POST"])
def analyse_lap_upload():
    data = request.get_json()
    if not isinstance(data, dict):
        return jsonify({"error": "Expected JSON object"}), 400

    laps = data.get("cleaned")

    if not isinstance(laps, list):
        return jsonify({"error": "Expected 'laps' to be a list"}), 400

    if len(laps) <= 1:
        return jsonify({"error": "Expected at least 2 clean laps to compare"}), 400

    sorted_laps = sorted(laps, key=lambda lap: lap.get("lapTime", float("inf")))
    fastest_lap = sorted_laps[0] if sorted_laps else None
    reference_laps = sorted_laps[1:] 

    fastest_samples = fastest_lap.get("samples", []) if fastest_lap else []
    reference_samples = reference_laps.get("samples", []) if reference_laps else []

    corners_by_position = build_reference_lap(rest_of_laps)

    # access keys match all laps corners by index
    #for corner_num, corners in corners_by_position.items():
    #    print("corner num", corner_num, "corners", corners_by_position )

    fast_matched_corners = analyse_lap(fastest_samples, None) 
    reference_matched_corners = analyse_lap(reference_samples, fast_matched_corners)

    matched_corners = match_zones(fast_matched_corners, reference_matched_corners) 
    #print("matched_corners", matched_corners)
    track_map = create_track_map(fastest_samples)
    lap_dist = get_lap_dist(fastest_samples)
    track_map_and_sectors = add_sectors_track_map(
        [m for m in fast_matched_corners],
        track_map,
    )

    coach = coaching(matched_corners, lap_dist)

    return jsonify({"coaching": coach, "track_map": track_map_and_sectors })
                    
