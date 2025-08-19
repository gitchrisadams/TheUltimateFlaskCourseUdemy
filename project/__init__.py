from flask import Flask
from .views.main import main
from .views.api import api
from .extensions import db


def create_app(config_file="settings.py"):
    app = Flask(__name__)

    # Configure env vars from .env file
    app.config.from_pyfile(config_file)

    # Initialize the db with app
    db.init_app(app)

    # Registers main route from routes.py
    app.register_blueprint(main)

    # Register api route blueprint the /api says
    # that when we access this route, it will be /api
    app.register_blueprint(api, url_prefix="/api")

    return app
