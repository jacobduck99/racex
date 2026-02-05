from flask import Blueprint, request, jsonify, session
import traceback

analyse_bp = Blueprint("analyse", __name__)

print("lap_data_routes.py loaded!")

@analyse_bp.route("/lap-data/analyse", methods=["POST"])
def analyse_lap_upload():
    try:
        data = request.get_json()

        if not data or not isinstance(data, list):
            return {"error": "Invalid data"}, 400

        max_speed = 0.0
        max_dist = 0.0
        max_lap = 0

        first_lap_change = None

        prev_lap = data[0]["lap"]

        for i, sample in enumerate(data):
            speed = sample["speed"]
            dist = sample["dist"]
            lap = sample["lap"]
            t = sample["t"]

            if speed > max_speed:
                max_speed = speed

            if dist > max_dist:
                max_dist = dist

            if lap > max_lap:
                max_lap = lap

            if lap != prev_lap and first_lap_change is None:
                first_lap_change = {
                    "index": i,
                    "from": prev_lap,
                    "to": lap,
                    "session_time": t,
                }

            prev_lap = lap

        print("=" * 60)
        print("TOTAL SAMPLES:", len(data))
        print("MAX SPEED:", max_speed)
        print("MAX DIST:", max_dist)
        print("MAX LAP:", max_lap)
        print("FIRST LAP CHANGE:", first_lap_change)
        print("=" * 60)

        return {
            "samples": len(data),
            "maxSpeed": max_speed,
            "maxDist": max_dist,
            "maxLap": max_lap,
            "firstLapChange": first_lap_change,
        }

    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"error": str(e)}, 500

