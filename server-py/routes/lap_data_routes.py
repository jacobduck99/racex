from flask import Blueprint, request, jsonify

analyse_bp = Blueprint("analyse", __name__)

@analyse_bp.route("/lap-data/analyse", methods=["POST"])
def analyse_lap_upload():
    print("route hit!")
    data = request.get_json()

    if not data or "lapTimes" not in data or not isinstance(data["lapTimes"], list):
        return jsonify({"error": "Invalid data"}), 400

    lap_times = data["lapTimes"]
    print("lap times:", lap_times)

    return jsonify({
        "laps": len(lap_times),
        "lapTimes": lap_times,
    })

