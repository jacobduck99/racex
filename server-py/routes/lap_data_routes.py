from flask import Blueprint, request, jsonify

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
    fastest_samples = fastest_lap.get("samples", []) if fastest_lap else []

    print("fastest lapTime:", fastest_lap.get("lapTime") if fastest_lap else None)
    print("fastest samples count:", len(fastest_samples))

    return jsonify({
        "laps": len(laps),
        "fastestLapTime": fastest_lap.get("lapTime") if fastest_lap else None,
        "fastestLapSamples": len(fastest_samples),
    })
