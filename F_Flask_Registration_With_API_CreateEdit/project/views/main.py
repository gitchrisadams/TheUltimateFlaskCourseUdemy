from datetime import datetime
from ..extensions import db
from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..models import Language, Topic, Member

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

    errors = {}

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

        # Form validation dictionary
        if not email:
            errors["email"] = "You must have an email address."
        if not password and not member_id:
            errors["password"] = "You must have a password."
        if not location:
            errors["location"] = "You must have a location"
        if not first_learn_date:
            errors["first_learn_date"] = "You must have first learn date."
        if not about:
            errors["about"] = "You must have an about section."
        if not interest_in_topics:
            errors["interest_in_topics"] = "You must choose at least one topic."

        # Check that we have no errors
        if not errors:
            # Check if member already exists, and if so, do an edit vs new member
            if member:
                member.email = email
                if password:
                    member.password = password
                member.location = location
                # Convert first_learn_date to a date w/ a format Year-Month-Day
                member.first_learn_date = datetime.strptime(
                    first_learn_date, "%Y-%m-%d"
                )
                member.fav_language = fav_language
                member.about = about
                member.learn_new_interest = (
                    True if learn_new_interest == "yes" else False
                )

                # Clear out all the topics
                member.interest_in_topics[:] = []
            else:
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

            # Loop through all topics and append topic to members
            for topic_id in interest_in_topics:
                topic = Topic.query.get(int(topic_id))
                member.interest_in_topics.append(topic)

            db.session.commit()

            # Redirect back to main page and use member_id if we have one so /1 /2 etc..
            # So can edit their profile if there is one vs seeing new form.
            return redirect(url_for("main.index", member_id=member.id))

    languages = Language.query.all()
    topics = Topic.query.all()

    # Create context so we can unpack and send to form
    # These variables are available in the template i.e. form.html
    context = {
        "member_id": member_id,
        "languages": languages,
        "topics": topics,
        "member": member,
        "errors": errors,
    }

    # Passed the languages/topics to context
    return render_template("form.html", **context)
