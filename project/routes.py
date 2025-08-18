from flask import Blueprint, render_template
from .extensions import db

main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("form.html")
