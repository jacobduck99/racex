from flask import Blueprint, request, jsonify, session
import traceback

analyse_bp = Blueprint("analyse", __name__)

print("lap_data_routes.py loaded!")

@analyse_bp.route("/lap-data/analyse", methods=["POST"])
def analyse_lap_upload():
    print("ROUTE HIT!")
    print("=" * 50)
    
    try:
        data = request.get_json(force=True) or {}
        print("here's your data", data)

        if not data:
            print("Missing file!")
            return jsonify({
                "error": "Missing file",
                "received": data,
            }), 400
        
        
        return jsonify({"ok": True, "message": "received"})
        
    except Exception as e:
        print(f" ERROR: {e}")
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
