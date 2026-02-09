from flask import Blueprint, request, jsonify

analyse_bp = Blueprint("analyse", __name__)

@analyse_bp.route("/lap-data/analyse", methods=["POST"])
def analyse_lap_upload():
    data = request.get_json()

    if not data or "lapTimes" not in data or not isinstance(data["lapTimes"], list):
        return jsonify({"error": "Invalid data"}), 400

    lap_times = data["lapTimes"]
    human_readable_laps = [round(t, 3) for t in lap_times]
    sorted_laps = sorted(human_readable_laps)
    print("lap times:", sorted_laps)
    
    compare_laps = []
    fastest_lap = sorted_laps[0]
    second_fastest_lap = sorted_laps[1]

    compare_laps.append(fastest_lap)
    compare_laps.append(second_fastest_lap)
    print("here are your laps to compare", compare_laps)
    
        

    return jsonify({
        "laps": len(lap_times),
        "lapTimes": compare_laps,
    })

