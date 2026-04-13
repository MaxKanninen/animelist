import sqlite3
import db

def create_user(username, password_hash):
    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
        return True
    except sqlite3.IntegrityError:
        return False

def get_user(username):
    sql = "SELECT id, password_hash FROM users WHERE username = ?"
    result = db.query(sql, [username])
    return result[0] if result else None