from flask import Flask, abort, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
import secrets
import config, series, users

app = Flask(__name__)
app.secret_key = config.secret_key

def require_login():
    if "user_id" not in session:
        abort(403)

def check_csrf():
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/registration", methods=["GET", "POST"])
def registration():
    if request.method == "GET":
        return render_template("registration.html")

    username = request.form["username"]
    if not username or len(username) >= 16:
        abort(403)
    if username.startswith(" "):
        return "Username cannot start with a space"
    password1 = request.form["password1"]
    if not password1 or len(password1) > 100:
        abort(403)
    password2 = request.form["password2"]

    if password1 != password2:
        return "Passwords don't match"
    
    if password1.startswith(" "):
        return "Password cannot start with a space"
    
    password_hash = generate_password_hash(password1)
    
    if users.create_user(username, password_hash):
        return "User registration completed"
    else:
        return "Username already taken"
    
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    username = request.form["username"]
    password = request.form["password"]

    user = users.get_user(username)
    if user and check_password_hash(user["password_hash"], password):
        session["user_id"] = user["id"]
        session["csrf_token"] = secrets.token_hex(16)
        return redirect("/")
    return "Wrong username or password"

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/add-series", methods=["GET", "POST"])
def add_series():
    require_login()

    if request.method == "GET":
        return render_template("add-series.html")
    
    check_csrf()
    
    title = request.form["title"]
    if not title or len(title) > 100:
        abort(403)
    description = request.form["description"]
    if not description or len(description) > 5000:
        abort(403)
    year = request.form["year"]
    try:
        year = int(year)
    except ValueError:
        abort(403)
    if year < 1 or year > 9999:
        abort(403)
    episodes = request.form["episodes"]
    try:
        episodes = int(episodes)
    except ValueError:
        abort(403)
    if episodes < 1 or episodes > 9999:
        abort(403)

    series.add_series(title, description, year, episodes, session["user_id"])
    return "Anime series added"

@app.route("/series")
def series_list():
    series_list = series.get_all_series()
    return render_template("series-list.html" , series_list=series_list)

@app.route("/series/<int:series_id>")
def series_page(series_id):
    result = series.get_series(series_id)
    if not result:
        abort(404)
    series_item = result[0]
    return render_template("series.html", series=series_item)

@app.route("/edit-series/<int:series_id>", methods=["GET", "POST"])
def edit_series(series_id):
    require_login()

    result = series.get_series(series_id)
    if not result:
        abort(404)
    series_item = result[0]
    if series_item["user_id"] != session.get("user_id"):
        abort(403)

    if request.method == "GET":
        return render_template("edit-series.html", series=series_item)
    
    check_csrf()

    title = request.form["title"]
    if not title or len(title) > 100:
        abort(403)
    description = request.form["description"]
    if not description or len(description) > 5000:
        abort(403)
    try:
        year = int(request.form["year"])
    except ValueError:
        abort(403)
    if year < 1 or year > 9999:
        abort(403)
    try:
        episodes = int(request.form["episodes"])
    except ValueError:
        abort(403)
    if episodes < 1 or episodes > 9999:
        abort(403)

    series.edit_series(title, description, year, episodes, series_id)
    return redirect("/series/" + str(series_id))

@app.route("/delete-series/<int:series_id>", methods=["POST"])
def delete_series(series_id):
    require_login()

    check_csrf()

    result = series.get_series(series_id)
    if not result:
        abort(404)
    if result[0]["user_id"] != session["user_id"]:
        abort(403)
    series.delete_series(series_id)
    return redirect("/series")

@app.route("/search")
def search():
    query = request.args.get("query")
    if query and len(query) > 100:
        abort(403)
    if query:
        results = series.search_series(query)
    else:
        results = []
    return render_template("search.html", query=query, results=results)