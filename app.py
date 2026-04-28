import math
import secrets

import markupsafe
from flask import Flask, abort, flash, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
import config
import db
import series
import users

app = Flask(__name__)
app.secret_key = config.secret_key

@app.template_filter()
def show_lines(content):
    content = str(markupsafe.escape(content))
    content = content.replace("\n", "<br />")
    return markupsafe.Markup(content)

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
        genres = series.get_all_genres()
        return render_template("add-series.html", genres=genres, selected_ids=[], filled={})

    check_csrf()

    title = request.form["title"]
    description = request.form["description"]
    year = request.form["year"]
    episodes = request.form["episodes"]
    genre_ids_raw = request.form.getlist("genres")

    try:
        genre_ids = [int(g) for g in genre_ids_raw]
    except ValueError:
        abort(403)

    filled = {"title": title, "description": description, "year": year, "episodes": episodes}
    all_genres = series.get_all_genres()

    def error(msg):
        flash(msg)
        return render_template("add-series.html", filled=filled,
                               genres=all_genres, selected_ids=genre_ids)

    if not title:
        return error("No title entered")
    if len(title) > 100:
        return error("Title too long (max 100 characters)")
    if not description:
        return error("No description entered")
    if len(description) > 5000:
        return error("Description too long (max 5000 characters)")
    try:
        year = int(year)
    except ValueError:
        return error("Invalid release year entered")
    if year < 1900 or year > 2050:
        return error("Invalid release year (needs to be between 1900-2050)")
    try:
        episodes = int(episodes)
    except ValueError:
        return error("Invalid episode amount entered")
    if episodes < 1 or episodes > 9999:
        return error("Invalid amount of episodes (needs to be between 1-9999)")

    series.add_series(title, description, year, episodes, session["user_id"])
    series.set_series_genres(db.last_insert_id(), genre_ids)
    flash("Anime added successfully")
    return redirect("/series")

@app.route("/series")
@app.route("/series/page/<int:page>")
def series_list(page=1):
    series_count = series.get_series_count()
    page_size = 10
    page_count = math.ceil(series_count / page_size)
    page_count = max(page_count, 1)

    if page < 1:
        return redirect("/series/page/1")
    if page > page_count:
        return redirect("/series/page/" + str(page_count))

    all_series = series.get_all_series(page, page_size)
    return render_template("series-list.html",
                           series_list=all_series, page=page, page_count=page_count)

@app.route("/series/<int:series_id>")
def series_page(series_id):
    result = series.get_series(series_id)
    if not result:
        abort(404)
    series_item = result[0]
    genres = series.get_series_genres(series_id)
    rating = series.get_series_rating(series_id)
    reviews = series.get_series_reviews(series_id)
    user_review = None
    if "user_id" in session:
        user_review = series.get_user_review(session["user_id"], series_id)
    return render_template("series.html", series=series_item, genres=genres,
                           rating=rating, reviews=reviews, user_review=user_review)

@app.route("/edit-series/<int:series_id>", methods=["GET", "POST"])
def edit_series(series_id):
    require_login()

    result = series.get_series(series_id)
    if not result:
        abort(404)
    series_item = result[0]
    if series_item["user_id"] != session.get("user_id"):
        abort(403)

    all_genres = series.get_all_genres()

    if request.method == "GET":
        filled = {"title": series_item["title"], "description": series_item["description"],
                  "year": series_item["year"], "episodes": series_item["episodes"]}
        selected_ids = [row["id"] for row in series.get_series_genres(series_id)]
        return render_template("edit-series.html", series=series_item, filled=filled,
                               genres=all_genres, selected_ids=selected_ids)

    check_csrf()

    title = request.form["title"]
    description = request.form["description"]
    year = request.form["year"]
    episodes = request.form["episodes"]
    genre_ids_raw = request.form.getlist("genres")
    try:
        genre_ids = [int(g) for g in genre_ids_raw]
    except ValueError:
        abort(403)

    filled = {"title": title, "description": description, "year": year, "episodes": episodes}

    def error(msg):
        flash(msg)
        return render_template("edit-series.html", series=series_item, filled=filled,
                               genres=all_genres, selected_ids=genre_ids)

    if not title:
        return error("No title entered")
    if len(title) > 100:
        return error("Title too long (max 100 characters)")
    if not description:
        return error("No description entered")
    if len(description) > 5000:
        return error("Description too long (max 5000 characters)")
    try:
        year = int(year)
    except ValueError:
        return error("Invalid release year entered")
    if year < 1900 or year > 2050:
        return error("Invalid release year (needs to be between 1900-2050)")
    try:
        episodes = int(episodes)
    except ValueError:
        return error("Invalid episode amount entered")
    if episodes < 1 or episodes > 9999:
        return error("Invalid amount of episodes (needs to be between 1-9999)")

    series.edit_series(title, description, year, episodes, series_id)
    series.set_series_genres(series_id, genre_ids)
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

@app.route("/series/<int:series_id>/review", methods=["GET", "POST"])
def add_review(series_id):
    require_login()

    result = series.get_series(series_id)
    if not result:
        abort(404)
    series_item = result[0]

    if series.get_user_review(session["user_id"], series_id):
        flash("You have already reviewed this series")
        return redirect("/series/" + str(series_id))

    if request.method == "GET":
        return render_template("review.html", series=series_item, filled={})

    check_csrf()

    rating = request.form["rating"]
    body = request.form["body"]

    filled = {"rating": rating, "body": body}

    def error(msg):
        flash(msg)
        return render_template("review.html", series=series_item, filled=filled)

    if rating not in ("1", "2", "3", "4", "5"):
        return error("Rating must be between 1 and 5")
    if not body:
        return error("No review entered")
    if len(body) > 5000:
        return error("Review too long (max 5000 characters)")

    series.add_review(rating, body, session["user_id"], series_id)
    flash("Review added successfully")
    return redirect("/series/" + str(series_id))

@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user_by_id(user_id)
    if not user:
        abort(404)
    stats = users.get_user_stats(user_id)
    user_series = users.get_user_series(user_id)
    return render_template("user.html", user=user, stats=stats, user_series=user_series)

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
