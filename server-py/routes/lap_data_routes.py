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

    lap_times = []
    for lap in laps:
        lap_time = lap.get("lapTime")
        lap_times.append(lap_time)
    print("here's your lap times", lap_times)

    sorted_laps = sorted(lap_times)
    print("here's your sorted laps", sorted_laps)

    return jsonify({
        "laps": len(laps),
        "firstLapTime": laps[0].get("lapTime") if laps else None,
        "firstLapSamples": len(laps[0].get("samples", [])) if laps else 0,
        "uniqueLapTimes": len(lap_times),
    })
