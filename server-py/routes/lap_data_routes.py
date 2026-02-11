from flask import Blueprint, request, jsonify
import json

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
    second_fastest_lap = sorted_laps[1] if sorted_laps else None
    fastest_samples = fastest_lap.get("samples", []) if fastest_lap else []
    second_fastest_samples = second_fastest_lap.get("samples", []) if second_fastest_lap else []

    fast_lap_braking = []
    fast_lap_brake_release = []
    braking = False

    for sample in fastest_samples:
        if not braking and sample["brake"] >= 0.01:
            fast_lap_braking.append(sample)
            braking = True
        elif braking == True and sample["brake"] < 0.01:
            fast_lap_brake_release.append(sample)
            braking = False
    
    second_fast_lap_braking = []
    second_fast_lap_brake_release = []

    fast_lap_pct = fast_lap_braking[0]["pct"]
    print("here's your fast lap pct", fast_lap_pct)
    fast_lap_braking_pct = fast_lap_brake_release[0]["pct"]
    print("here's your braking fast lap pct", fast_lap_braking_pct)

    fast_lap_braking_dist = fast_lap_braking_pct - fast_lap_pct 
    print("here's your braking distance", fast_lap_braking_dist)

    for sample in second_fastest_samples:
        if not braking and sample["brake"] >= 0.01:
            second_fast_lap_braking.append(sample)
            braking = True
        elif braking == True and sample["brake"] < 0.01:
            second_fast_lap_brake_release.append(sample)
            braking = False

    print("here's your fastest lap samples for t1 \n", fast_lap_braking)
    print("here's when you release the brake for fast lap \n", fast_lap_brake_release)

    print("here's your second fast lap samples for t1 \n", second_fast_lap_braking)
    print("here's when you release the brake for second fastest lap", second_fast_lap_brake_release)

    print("fastest lapTime:", fastest_lap.get("lapTime") if fastest_lap else None)
    print("fastest samples count:", len(fastest_samples))

    print("second fastest lapTime:", second_fastest_lap.get("lapTime") if second_fastest_lap else None)
    print("second fastest sample count:", len(second_fastest_samples))

    return jsonify({
        "laps": len(laps),
        "fastestLapTime": fastest_lap.get("lapTime") if fastest_lap else None,
        "fastestLapSamples": len(fastest_samples),
    })
