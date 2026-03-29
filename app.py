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
    return "hello world"

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
            session["username"] = username
            session["csrf_token"] = secrets.token_hex(16)
            return redirect("/")

    return "Wrong username or password"