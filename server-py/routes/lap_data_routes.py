from flask import Blueprint, request, jsonify, session
import traceback

analyse_bp = Blueprint("analyse", __name__)

print("lap_data_routes.py loaded!")

@analyse_bp.route("/lap-data/analyse", methods=["POST"])
def analyse_lap_upload():
    print("ROUTE HIT!")
    print("=" * 50)
    
    try:
        print("1. Checking content type...")
        print("Content-Type:", request.content_type)
        
        print("2. Accessing request.files...")
        file = request.files
        print("Files received:", list(file.keys()))
        
        print("3. Accessing request.form...")
        print("Form keys:", list(request.form.keys()))
        
        print("4. Getting file objects...")
        race_session = file.get("raceSession")
        if not race_session:
            print("Missing file!")
            return jsonify({
                "error": "Missing file",
                "received": list(file.keys())
            }), 400
        
        print(f"5. Files found: {race_session.filename}")
        
        return jsonify({"ok": True, "message": "File received"})
        
    except Exception as e:
        print(f" ERROR: {e}")
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
