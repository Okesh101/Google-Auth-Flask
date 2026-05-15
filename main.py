from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from database.db import init_db
import os


load_dotenv()

FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY")
FLASK_ENV = os.getenv("FLASK_ENV")


def initialize_app():
    app = Flask(__name__)
    CORS(app, supports_credentials=True)
    app.config["SECRET_KEY"] = FLASK_SECRET_KEY
    return app


def create_app(app):
    from routes.auth import auth_bp
    from routes.health import health_bp
    from routes.admin import admin_bp
    from routes.google import google_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(health_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(google_bp)

    return app


if FLASK_ENV == "production":
    init_db()
    init_app = initialize_app()
    app = create_app(init_app)

if __name__ == "__main__":
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        init_db()
    init_app = initialize_app()
    app = create_app(init_app)
    app.run(debug=True, use_reloader=True)
