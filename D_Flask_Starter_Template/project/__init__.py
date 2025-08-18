from flask import Flask
from .routes import main
from .extensions import db


def create_app():
    app = Flask(__name__)

    # Configure env vars from .env file
    app.config.from_prefixed_env()

    # Initialize the db with app
    db.init_app(app)

    # Registers main route from routes.py
    app.register_blueprint(main)

    return app
