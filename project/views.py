from .extensions import db
from flask import Blueprint, render_template, request
from .models import Language, Topic

main = Blueprint("main", __name__)


@main.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get all the form input
        email = request.form["email"]
        password = request.form["password"]
        location = request.form["location"]
        first_learn_date = request.form["first_learn_date"]
        fav_language = request.form["fav_language"]
        about = request.form["about"]
        learn_new_interest = request.form["learn_new_interest"]
        interest_in_topics = request.form.getlist("interest_in_topics")

        print("email", email)
        print("password", password)
        print("location", location)
        print("first_learn_date", first_learn_date)
        print("fav_language", fav_language)
        print("about", about)
        print("learn_new_interest", learn_new_interest)
        print("interest_in_topics", interest_in_topics)

        return "Form Submitted!"

    languages = Language.query.all()
    topics = Topic.query.all()

    # Create context so we can unpack and send to form
    context = {"languages": languages, "topics": topics}

    # Passed the languages/topics to context
    return render_template("form.html", **context)
