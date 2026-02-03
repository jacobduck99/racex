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
        files = request.files
        print("Files received:", list(files.keys()))
        
        print("3. Accessing request.form...")
        print("Form keys:", list(request.form.keys()))
        
        print("4. Getting file objects...")
        fast_lap_file = files.get('fastLapFile')
        avg_lap_file = files.get('avgLapFile')
        
        if not fast_lap_file or not avg_lap_file:
            print("Missing files!")
            return jsonify({
                "error": "Missing files",
                "received": list(files.keys())
            }), 400
        
        print(f"5. Files found: {fast_lap_file.filename}, {avg_lap_file.filename}")
        
        return jsonify({"ok": True, "message": "Files received"})
        
    except Exception as e:
        print(f" ERROR: {e}")
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
