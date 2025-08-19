from flask import Blueprint, jsonify
from project.models import Member

api = Blueprint("api", __name__)


@api.route("/member", methods=["GET"])
def get_members():
    """
    Gets all members in json format

    Returns:
        object: All members in json format
    """
    # Get all the members
    members = Member.query.all()

    # Call member_to_json with a list comprehension and jsonify it in members key:
    return jsonify({"members": [member.member_to_json() for member in members]})


@api.route("/member/<int:member_id>", methods=["GET"])
def get_member(member_id):
    """
    Gets a single member in json format.

    Args:
        member_id (int): The id of the member.

    Returns:
        object: The member in json format.
    """
    member = Member.query.get(member_id)
    return jsonify({"member": member.member_to_json()})
