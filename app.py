from flask import Flask
from flask import abort, redirect, render_template, request, session
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash
import secrets
import config, db

app = Flask(__name__)
app.secret_key = config.secret_key

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
    password2 = request.form["password2"]

    if password1 != password2:
        return "Passwords don't match"
    
    if password1.startswith(" "):
        return "Password cannot start with a space"
    
    password_hash = generate_password_hash(password1)
    
    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
        return "User registration completed"
    except sqlite3.IntegrityError:
        return "Username already taken"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    username = request.form["username"]
    password = request.form["password"]

    sql = "SELECT id, password_hash FROM users WHERE username = ?"
    result = db.query(sql, [username])

    if len(result) == 1:
        user = result[0]
        if check_password_hash(user["password_hash"], password):
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
    if request.method == "GET":
        return render_template("add-series.html")
    
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
    if not year or 1 > year > 9999:
        abort(403)
    episodes = request.form["episodes"]
    try:
        episodes = int(episodes)
    except ValueError:
        abort(403)
    if not episodes or 1 > episodes > 9999:
        abort(403)

    sql = "INSERT INTO series (title, description, year, episodes) VALUES (?, ?, ?, ?)"
    db.execute(sql, [title, description, year, episodes])
    return "Anime series added"