from flask import Blueprint, request, jsonify

analyse_bp = Blueprint("analyse", __name__)

@analyse_bp.route("/lap-data/analyse", methods=["POST"])
def analyse_lap_upload():
    data = request.get_json()

    if not isinstance(data, dict):
        return jsonify({"error": "Expected JSON object"}), 400

    laps = data.get("laps")
    if not isinstance(laps, list):
        return jsonify({"error": "Expected 'laps' to be a list", "gotType": str(type(laps))}), 400

    print("laps count:", len(laps))
    if len(laps) > 0:
        first = laps[0]
        print("first lap keys:", list(first.keys()) if isinstance(first, dict) else type(first))
        if isinstance(first, dict):
            print("first lapTime:", first.get("lapTime"))
            samples = first.get("samples", [])
            print("first samples count:", len(samples))
            if samples:
                print("first sample:", samples[0])

    return jsonify({
        "laps": len(laps),
        "firstLapTime": laps[0].get("lapTime") if laps and isinstance(laps[0], dict) else None,
        "firstLapSamples": len(laps[0].get("samples", [])) if laps and isinstance(laps[0], dict) else 0,
    })


