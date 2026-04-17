from flask import Flask, abort, flash, redirect, render_template, request, session
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
        return render_template("registration.html", filled={})

    username = request.form["username"]
    if not username:
        flash("No username entered")
        return render_template("registration.html", filled={})
    if len(username) > 16:
        flash("Username too long")
        return render_template("registration.html", filled={})
    if username.startswith(" "):
        flash("Username cannot start with a blank space")
        return render_template("registration.html", filled={})
    
    password1 = request.form["password1"]
    if not password1:
        flash("No password entered")
        filled = {"username": username}
        return render_template("registration.html", filled=filled)
    if len(password1) > 100:
        flash("Password too long (max 100 characters)")
        filled = {"username": username}
        return render_template("registration.html", filled=filled)
    password2 = request.form["password2"]

    if password1 != password2:
        flash("Passwords don't match")
        filled = {"username": username}
        return render_template("registration.html", filled=filled)
    
    if password1.startswith(" "):
        flash("Password cannot start with a blank space")
        filled = {"username": username}
        return render_template("registration.html", filled=filled)
    
    password_hash = generate_password_hash(password1)
    
    if users.create_user(username, password_hash):
        flash("User registration successful")
        return redirect("/")
    else:
        flash("Username already taken")
        return render_template("registration.html", filled={})
    
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
    flash("Wrong username or password")
    return redirect("/login")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/add-series", methods=["GET", "POST"])
def add_series():
    require_login()

    if request.method == "GET":
        return render_template("add-series.html", filled={})
    
    check_csrf()
    
    title = request.form["title"]
    description = request.form["description"]
    year = request.form["year"]
    episodes = request.form["episodes"]

    if not title:
        flash("No title entered")
        filled = {"title": title, "description": description, "year": year, "episodes": episodes}
        return render_template("add-series.html", filled=filled)
    if len(title) > 100:
        flash("Title too long (max 100 characters)")
        filled = {"title": title, "description": description, "year": year, "episodes": episodes}
        return render_template("add-series.html", filled=filled)
    if not description:
        flash("No description entered")
        filled = {"title": title, "description": description, "year": year, "episodes": episodes}
        return render_template("add-series.html", filled=filled)
    if len(description) > 5000:
        flash("Description too long (max 5000 characters)")
        filled = {"title": title, "description": description, "year": year, "episodes": episodes}
        return render_template("add-series.html", filled=filled)
    try:
        year = int(year)
    except ValueError:
        flash("Invalid release year entered")
        filled = {"title": title, "description": description, "year": year, "episodes": episodes}
        return render_template("add-series.html", filled=filled)
    if year < 1900 or year > 2050:
        flash("Invalid release year (needs to be between 1900-2050)")
        filled = {"title": title, "description": description, "year": year, "episodes": episodes}
        return render_template("add-series.html", filled=filled)
    try:
        episodes = int(episodes)
    except ValueError:
        flash("Invalid episode amount entered")
        filled = {"title": title, "description": description, "year": year, "episodes": episodes}
        return render_template("add-series.html", filled=filled)
    if episodes < 1 or episodes > 9999:
        flash("Invalid amount of episodes (needs to be between 1-9999)")
        filled = {"title": title, "description": description, "year": year, "episodes": episodes}
        return render_template("add-series.html", filled=filled)

    series.add_series(title, description, year, episodes, session["user_id"])
    flash("Anime added successfully")
    return redirect("/series")

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
        filled = {"title": series_item["title"], "description": series_item["description"],
                  "year": series_item["year"], "episodes": series_item["episodes"]}
        return render_template("edit-series.html", series=series_item, filled=filled)

    check_csrf()

    title = request.form["title"]
    description = request.form["description"]
    year = request.form["year"]
    episodes = request.form["episodes"]

    if not title:
        flash("No title entered")
        filled = {"title": title, "description": description, "year": year, "episodes": episodes}
        return render_template("edit-series.html", series=series_item, filled=filled)
    if len(title) > 100:
        flash("Title too long (max 100 characters)")
        filled = {"title": title, "description": description, "year": year, "episodes": episodes}
        return render_template("edit-series.html", series=series_item, filled=filled)
    if not description:
        flash("No description entered")
        filled = {"title": title, "description": description, "year": year, "episodes": episodes}
        return render_template("edit-series.html", series=series_item, filled=filled)
    if len(description) > 5000:
        flash("Description too long (max 5000 characters)")
        filled = {"title": title, "description": description, "year": year, "episodes": episodes}
        return render_template("edit-series.html", series=series_item, filled=filled)
    try:
        year = int(year)
    except ValueError:
        flash("Invalid release year entered")
        filled = {"title": title, "description": description, "year": year, "episodes": episodes}
        return render_template("edit-series.html", series=series_item, filled=filled)
    if year < 1900 or year > 2050:
        flash("Invalid release year (needs to be between 1900-2050)")
        filled = {"title": title, "description": description, "year": year, "episodes": episodes}
        return render_template("edit-series.html", series=series_item, filled=filled)
    try:
        episodes = int(episodes)
    except ValueError:
        flash("Invalid episode amount entered")
        filled = {"title": title, "description": description, "year": year, "episodes": episodes}
        return render_template("edit-series.html", series=series_item, filled=filled)
    if episodes < 1 or episodes > 9999:
        flash("Invalid amount of episodes (needs to be between 1-9999)")
        filled = {"title": title, "description": description, "year": year, "episodes": episodes}
        return render_template("edit-series.html", series=series_item, filled=filled)

    series.edit_series(title, description, year, episodes, series_id)
    flash("Anime edited successfully")
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
    flash("Anime successfully deleted")
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