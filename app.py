from flask import Flask, request, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy  # Lib to use SQL databases

app = Flask(__name__)

# Configure SQL Lite URI
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"

# Init sql db
db = SQLAlchemy(app)


class User(db.Model):
    """
    A class representing a user.
    A user can have many orders, but an order
    belongs to only one user.

    Attributes:
        id(int): The id of the user.
        name(str): The name of the user.
        date_joined(date): The date the user joined.
        orders(str): Relationship with the Orders table
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    date_joined = db.Column(db.DateTime)

    # Allows relationship with Order table, then can use
    # User.orders and get all orders associated w/ a user
    # The back_populates links it to the user table.
    orders = db.relationship("Order", back_populates=("user"))


class Order(db.Model):
    """
    A class representing an Order of the user.
    An user can have many orders but an order only
    belongs to one user.

    Attributes:
        id(int): The id of the user.
        total(int): The name of the user.
        user_id(int): The foreign key user.id in the User Table
        user(str): The relationship to the User table
    """

    id = db.Column(db.Integer, primary_key=True)
    total = db.Column(db.Integer)
    user_id = db.Column(
        db.ForeignKey("user.id")
    )  # This user_id refers to user.id in User table

    # This establishes a relationship with the User table
    # This allows you to do use order.user and get the order
    # associated w/ user, the back_populates links to the orders table
    user = db.relationship("User", back_populates=("orders"))


# Home / route
@app.route("/")
def index():
    """
    The route to the main root page or /.

    Returns:
        render_template: The rendered template page for the root page.
    """
    return render_template(
        "index.html", page_name="root route", page_num=2
    )  # page_name/num show on template page


# /home Route
@app.route("/home", methods=["GET"])
def home():
    """
    The route to home or /home.

    Returns:
        render_template: The rendered template page for home.html.
    """
    return render_template(
        "home.html", number=15, data=[{"key": "value1"}, {"key": "value3"}]
    )


# Returning JSON
@app.route("/json")
def json():
    """
    The route to the endpoint that returns json data

    Returns:
        object: json data.
    """
    return {"mykey": "JSON Value!", "mylist": [1, 2, 3, 4, 5]}


# Dynamic such as: http://localhost:5000/dynamic/chris returns "chris"
@app.route("/dynamic", defaults={"user_input": "default"})
@app.route("/dynamic/<user_input>")
def dynamic(user_input):
    """
    The route to the dynamic endpoint that shows the string passed in.

    Parameters:
        user_input(str): The string data to show on the web page.

    Returns:
        object: The json data.
    """
    return f"<h1>The user entered: {user_input}</h1>"


# Query strings such as: http://localhost:5000/query?first=chris&second=christian
@app.route("/query")
def query():
    """
    The route to the /query endpont that accepts query parameters.
    They should be in the format of first= and second= with a value
    for each.

    Returns:
        str: The formatted string with first and second values.
    """
    first = request.args.get("first")
    second = request.args.get("second")
    return f"<h1>The query string contains: {first} and {second}</h1>"


# Sending form data
@app.route("/form", methods=["GET", "POST"])
def form():
    """
    The route to the /form endpoint. Submits form data
    inputted by the user.

    Returns:
        redirect: The page to redirect to if a POST
    """
    if request.method == "POST":
        user_input = request.form["user_input"]
        print(user_input)
        return redirect(url_for("home"))  # Example of redirecting to home page

    return '<form method="POST"><input type="text" name="user_input" /><input type="submit" /></form>'


# Accepts Json input such as:
# {
#         "hello": "world!",
#         "mylist": [1, 3, 4, 6]
# }
@app.route("/acceptjson")
def acceptjson():
    """
    The route to the /acceptsjson endpoit. This
    accepts json data.

    Returns:
        object: api_input and hello
    """
    json_data = request.get_json()
    api_input = json_data["mylist"]
    hello = json_data["hello"]
    return {"api_input": api_input, "hello": hello}


# Used to test an error when in debug mode vs debug mode off
@app.route("/error")
def error():
    """
    The error endpoint.

    Returns:
        error: The error to return
    """
    a = 1 / 0
    return "Error"


# Inserting data into database
def insert_data():
    """
    Insert data into Users database table.
    """
    from datetime import datetime

    # Create a new user w/ timestamp
    python_user = User(name="Python User", date_joined=datetime.now())
    flask_user = User(name="Flask User", date_joined=datetime.now())
    javascript_user = User(name="Javascript User", date_joined=datetime.now())

    # All all users to db:
    db.session.add_all([python_user, flask_user, javascript_user])

    # Add a new user to db
    # db.session.add(new_user)

    # Add new orders to db:
    first_order = Order(total=99, user=python_user)
    second_order = Order(total=20, user=python_user)
    third_order = Order(total=199, user=flask_user)

    # Add All orders to db:
    db.session.add_all([first_order, second_order, third_order])

    # Commit/Save all changes to db
    db.session.commit()


# Inserting data into a database
def update_data():
    """
    Update data in the Users database table.
    """
    # Get the first user:
    user = User.query.first()

    # Change the name
    user.name = "Flask user"
    db.session.commit()


# Deleting data
def delete_data():
    """
    Delete data in the Users the database table.
    """
    # Get the first user:
    user = User.query.first()

    # Delete the user
    db.session.delete(user)
    db.session.commit()
