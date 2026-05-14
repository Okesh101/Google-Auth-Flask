from flask import Flask
from flask_cors import CORS
from flask_session import Session
from datetime import timedelta
from dotenv import load_dotenv
from database.db import init_db
import os

load_dotenv()

FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY")
FLASK_ENV = os.getenv("FLASK_ENV")
SESSION_TYPE = os.getenv("SESSION_TYPE")


def initialize_app():
    app = Flask(__name__)
    CORS(app, supports_credentials=True)
    app.config["SECRET_KEY"] = FLASK_SECRET_KEY
    app.config["SESSION_TYPE"] = SESSION_TYPE # determines where session data is stored (filesystem, redis, database, etc.)
    app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=30) # Session will expire after 30 minutes of inactivity
    Session(app)
    return app


def create_app(app):
    from routes.auth import auth_bp
    from routes.health import health_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(health_bp)

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
