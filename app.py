from flask import Flask
from flask import abort, render_template, request
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash
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
    
    if request.method == "POST":
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