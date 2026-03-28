from flask import Flask
import config, db

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    return "hello world"