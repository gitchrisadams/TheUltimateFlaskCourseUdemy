from flask import Flask
from .views.main import main
from .extensions import db


def create_app(config_file="settings.py"):
    app = Flask(__name__)

    # Configure env vars from .env file
    app.config.from_pyfile(config_file)

    # Initialize the db with app
    db.init_app(app)

    # Registers main route from routes.py
    app.register_blueprint(main)

    return app
