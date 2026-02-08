from flask import Blueprint, request, jsonify
import traceback

analyse_bp = Blueprint("analyse", __name__)

print("lap_data_routes.py loaded!")

@analyse_bp.route("/lap-data/analyse", methods=["POST"])
def analyse_lap_upload():
    try:
        data = request.get_json()

        if not data or not isinstance(data, list):
            return {"error": "Invalid data"}, 400

        total_laps = len(data)
        total_samples = 0

        max_speed = 0.0
        max_dist = 0.0
        fastest_lap = None

        lap_summaries = []

        for lap_index, lap in enumerate(data, start=1):
            lap_time = lap.get("lapTime")
            samples = lap.get("samples", [])

            if lap_time is None or not samples:
                continue

            total_samples += len(samples)

            # Track fastest lap
            if fastest_lap is None or lap_time < fastest_lap["lapTime"]:
                fastest_lap = {
                    "lap": lap_index,
                    "lapTime": lap_time,
                }

            # Scan samples inside the lap
            for s in samples:
                speed = s.get("speed", 0.0)
                dist = s.get("dist", 0.0)

                if speed > max_speed:
                    max_speed = speed

                if dist > max_dist:
                    max_dist = dist

            lap_summaries.append({
                "lap": lap_index,
                "lapTime": round(lap_time, 3),
                "samples": len(samples),
            })

        print("=" * 60)
        print("TOTAL LAPS:", total_laps)
        print("TOTAL SAMPLES:", total_samples)
        print("FASTEST LAP:", fastest_lap)
        print("MAX SPEED:", max_speed)
        print("MAX DIST:", max_dist)
        print("LAP SUMMARY:")
        for s in lap_summaries:
            print(f"  Lap {s['lap']}: {s['lapTime']}s ({s['samples']} samples)")
        print("=" * 60)

        return jsonify({
            "laps": total_laps,
            "samples": total_samples,
            "fastestLap": fastest_lap,
            "maxSpeed": max_speed,
            "maxDist": max_dist,
            "lapSummary": lap_summaries,
        })

    except Exception as e:
        traceback.print_exc()
        return {"error": str(e)}, 500


