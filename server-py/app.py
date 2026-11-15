# server/app.py
import os

from flask import Flask
from flask_cors import CORS
from routes.lap_data_routes import analyse_bp


def create_app():
    app = Flask(__name__)

    app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024

    CORS(
        app,
        resources={r"/api/*": {"origins": [
            "http://localhost:5173",
        ]}},
        supports_credentials=True,
    )

    app.register_blueprint(analyse_bp, url_prefix="/api")

    return app

app = create_app()

if __name__ == "__main__":
    # local dev only (production runs gunicorn, see Dockerfile).
    # FLASK_DEBUG=1 python app.py  -> debug mode
    debug = os.environ.get("FLASK_DEBUG") == "1"
    app.run(host="127.0.0.1", port=5000, debug=debug, use_reloader=False, threaded=True)
