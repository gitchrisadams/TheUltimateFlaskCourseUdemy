from datetime import datetime
from .extensions import db
from flask import Blueprint, render_template, request
from .models import Language, Topic, Member

main = Blueprint("main", __name__)


@main.route("/", methods=["GET", "POST"], defaults={"member_id": None})
@main.route("/<int:member_id>", methods=["GET", "POST"])
def index(member_id):
    """
    The Default root route of /.
    If No member_id is supplied, it defaults to None

    Args:
        member_id (str): The member id

    Returns:
        str: form submitted success message.
    """
    member = None
    if member_id:
        member = Member.query.get_or_404(member_id)

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

        # Create a new member
        member = Member(
            email=email,
            password=password,
            location=location,
            # Convert first_learn_date to a date w/ a format Year-Month-Day
            first_learn_date=datetime.strptime(first_learn_date, "%Y-%m-%d"),
            fav_language=fav_language,
            about=about,
            learn_new_interest=(True if learn_new_interest == "yes" else False),
        )

        # Add member to the DB
        db.session.add(member)

        # Loop through all topics and append topic to member
        for topic_id in interest_in_topics:
            topic = Topic.query.get(int(topic_id))
            member.interest_in_topics.append(topic)

        db.session.commit()

        return "Form Submitted!"

    languages = Language.query.all()
    topics = Topic.query.all()

    # Create context so we can unpack and send to form
    # These variables are available in the template i.e. form.html
    context = {
        "member_id": member_id,
        "languages": languages,
        "topics": topics,
        "member": member,
    }

    # Passed the languages/topics to context
    return render_template("form.html", **context)
