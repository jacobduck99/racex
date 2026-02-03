from flask import Blueprint, request, jsonify, session

analyse_bp = Blueprint("analyse", __name__)

@analyse_bp.post("/lap-data/analyse")
def analyse_lap_upload():
    return {"ok": True}
