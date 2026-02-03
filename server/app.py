# server/app.py
from flask import Flask
import routes.lap_data_routes.py import analyse_bp

def create_app():
    app = Flask(__name__)

    # Required for session cookies (Flask-Login)
    app.secret_key = "change-me-in-env"

    # Allow React dev server to send/receive cookies

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
    app.run(host="0.0.0.0", port=5000, debug=True)
