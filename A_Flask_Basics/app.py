from flask import Flask, request, redirect, url_for

app = Flask(__name__)


# Home / route
@app.route("/")
def index():
    return "<h1>Hello</h1>"


# /home Route
@app.route("/home", methods=["GET"])
def home():
    return "<h1>Home</h1>"


# Returning JSON
@app.route("/json")
def json():
    return {"mykey": "JSON Value!", "mylist": [1, 2, 3, 4, 5]}


# Dynamic such as: http://localhost:5000/dynamic/chris returns "chris"
@app.route("/dynamic", defaults={"user_input": "default"})
@app.route("/dynamic/<user_input>")
def dynamic(user_input):
    return f"<h1>The user entered: {user_input}</h1>"


# Query strings such as: http://localhost:5000/query?first=chris&second=christian
@app.route("/query")
def query():
    first = request.args.get("first")
    second = request.args.get("second")
    return f"<h1>The query string contains: {first} and {second}</h1>"


# Sending form data
@app.route("/form", methods=["GET", "POST"])
def form():
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
    json_data = request.get_json()
    api_input = json_data["mylist"]
    hello = json_data["hello"]
    return {"api_input": api_input, "hello": hello}


# Used to test an error when in debug mode vs debug mode off
@app.route("/error")
def error():
    a = 1 / 0
    return "Error"
