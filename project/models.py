from .extensions import db
from werkzeug.security import generate_password_hash
from datetime import datetime

# Create an association table to link Topics and members
member_topic_table = db.Table(
    "member_topic",
    db.Column("member_id", db.Integer, db.ForeignKey("member.id"), primary_key=True),
    db.Column("topic_id", db.Integer, db.ForeignKey("topic.id"), primary_key=True),
)


class Member(db.Model):
    """
    The Member class represents a member/user.
    Members have a many to many relationship.
    A Member can have many topics and a topic have many members.

    Attributes:
        id(int): The id of the member.
        email(str): The email of the member.
        password_hash(str): The password hash of the member.
        location(str): The location of the member.
        first_learn_date(date): The date the member learned to code.
        fav_language(int): The foreign key language id in the language table.
        about(str): The about information of the member.
    """

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))
    password_hash = db.Column(db.String(50))
    location = db.Column(db.String(30))
    first_learn_date = db.Column(db.DateTime)

    # languages are pulled as foreign key in language table
    fav_language = db.Column(db.ForeignKey("language.id"))

    about = db.Column(db.Text)
    learn_new_interest = db.Column(db.Boolean)

    interest_in_topics = db.relationship(
        "Topic",  # The Topic table
        secondary=member_topic_table,  # The variable above for member_topic_table association
        lazy=True,
        backref=db.backref("topic", lazy=True),
    )

    # @property allows us to access this like password.value
    @property
    def password(self):
        raise AttributeError("Cannot view password")

    @password.setter
    def password(self, password):
        """
        Generates password hash from a password

        Args:
            password (str): The password to hash
        """
        self.password_hash = generate_password_hash(password)

    def member_to_json(self):
        """
        Formats the members in json format, it gets all the members.
        Requst would look like this: http://localhost:5000/api/member

        Returns:
            object: The members formatted in json.
        """
        # Loop through topics and create a new dict with id and name
        topics = []
        for topic in self.interest_in_topics:
            topics.append({"id": topic.id, "name": topic.name})

        # Get the language id and name
        fav_language = Language.query.get(self.fav_language)
        language_json = {"id": fav_language.id, "name": fav_language.name}

        # Prepared json to return
        member_json = {
            "id": self.id,
            "email": self.email,
            "location": self.location,
            "first_learn_date": datetime.strftime(self.first_learn_date, "%Y-%m-%d"),
            "fav_language": language_json,
            "about": self.about,
            "learn_new_interest": self.learn_new_interest,
            "interest_in_topics": topics,
        }

        return member_json


class Language(db.Model):
    """
    The Language class represents a computer programming language

    Attributes:
        id(str): The id of the language
        name(str): The name of the language
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10))


class Topic(db.Model):
    """
    A Topic Class represents a Topic, such as
    Web apps, Mobile Apps, and Api's.s
    A Topic is a Many to Many relationship.
    A web app topic will have many users, and
    many users will have web apps topic.

    Attributes:
        id(str): The id of the Topic
        name(str): The name of the Topic
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
