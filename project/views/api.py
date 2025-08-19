from datetime import datetime
from flask import Blueprint, jsonify, request
from project.models import Member, Topic
from project.extensions import db

api = Blueprint("api", __name__)


@api.route("/member", methods=["GET"])
def get_members():
    """
    Gets all members in json format.
    Example: http://localhost:5000/api/member

    Returns:
        dict: All members in json format
    """
    # Get all the members
    members = Member.query.all()

    # Call member_to_json with a list comprehension and jsonify it in members key:
    return jsonify({"members": [member.member_to_json() for member in members]})


@api.route("/member/<int:member_id>", methods=["GET"])
def get_member(member_id):
    """
    Gets a single member in json format.
    Example: http://localhost:5000/api/member/1

    Args:
        member_id (int): The id of the member.

    Returns:
        dict: The member in json format.
    """
    member = Member.query.get(member_id)
    return jsonify({"member": member.member_to_json()})


@api.route("/member", methods=["POST"])
def create_member():
    """
    Creates a new member
    Use GET: Example: http://localhost:5000/api/member/1 to
    see example of POST data to include. Add password as well.

    Returns:
        dict: The member created in json format.
    """
    # Get all the data from requeset
    member_req_data = request.get_json()

    # Create a new member class with data from request
    member = Member(
        about=member_req_data.get("about"),
        email=member_req_data.get("email"),
        password=member_req_data.get("password"),
        fav_language=member_req_data["fav_language"].get("id"),
        first_learn_date=datetime.strptime(
            member_req_data.get("first_learn_date"), "%Y-%m-%d"
        ),
        location=member_req_data.get("location"),
        learn_new_interest=member_req_data.get("learn_new_interest"),
    )

    # Get data for topics and append to the member object
    interest_in_topics = member_req_data.get("interest_in_topics")

    for member_topic in interest_in_topics:
        topic = Topic.query.get(member_topic["id"])
        member.interest_in_topics.append(topic)

    db.session.add(member)
    db.session.commit()

    return jsonify({"member": member.member_to_json()})
