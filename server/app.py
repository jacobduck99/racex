# server/app.py
from flask import Flask
from flask_cors import CORS
from routes.lap_data_routes import analyse_bp


def create_app():
    app = Flask(__name__)

    app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024 

    # Required for session cookies (Flask-Login)
    app.secret_key = "change-me-in-env"

    # Allow React dev server to send/receive cookies

    CORS(
        app,
        resources={r"/api/*": {"origins": [
            "http://localhost:5173",
        ]}},
        supports_credentials=True,
    )

    # Cookie settings (dev-safe; tighten for prod/HTTPS)
    app.config.update(
        SESSION_COOKIE_HTTPONLY=True,
    )

    # Register blueprints exactly once
    app.register_blueprint(analyse_bp, url_prefix="/api")

    # Ensure DB connection closes after each request
   # app.teardown_appcontext(close_db)

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)
