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

def get_user_by_id(user_id):
    sql = "SELECT id, username FROM users WHERE id = ?"
    result = db.query(sql, [user_id])
    return result[0] if result else None

def get_user_stats(user_id):
    sql = "SELECT COUNT(*) count FROM series WHERE user_id = ?"
    series_count = db.query(sql, [user_id])[0]["count"]
    sql = """SELECT COUNT(*) count, AVG(rating) avg_rating
             FROM reviews WHERE user_id = ?"""
    reviews = db.query(sql, [user_id])[0]
    return {"series_count": series_count,
            "reviews_count": reviews["count"],
            "avg_rating": reviews["avg_rating"]}

def get_user_series(user_id):
    sql = """SELECT id, title, year, episodes
             FROM series
             WHERE user_id = ?
             ORDER BY created_at DESC"""
    return db.query(sql, [user_id])
