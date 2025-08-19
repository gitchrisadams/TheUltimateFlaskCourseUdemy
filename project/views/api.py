from flask import Blueprint, jsonify
from project.models import Member

api = Blueprint("api", __name__)


@api.route("/member", methods=["GET"])
def get_members():
    # Get all the members
    members = Member.query.all()

    # Call member_to_json with a list comprehension and jsonify it in members key:
    return jsonify({"members": [member.member_to_json() for member in members]})
