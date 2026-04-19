import db

def add_series(title, description, year, episodes, user_id):
    sql = """INSERT INTO series (title, description, year, episodes, user_id, created_at)
             VALUES (?, ?, ?, ?, ?, datetime('now'))"""
    db.execute(sql, [title, description, year, episodes, user_id])

def edit_series(title, description, year, episodes, series_id):
    sql = """UPDATE series
             SET title = ?, description = ?, year = ?, episodes = ?
             WHERE id = ?"""
    db.execute(sql, [title, description, year, episodes, series_id])

def set_series_genres(series_id, genre_id_list):
    sql = "DELETE FROM series_genres WHERE series_id = ?"
    db.execute(sql, [series_id])
    for genre_id in genre_id_list:
        sql = "INSERT INTO series_genres (series_id, genre_id) VALUES (?, ?)"
        db.execute(sql, [series_id, genre_id])

def delete_series(series_id):
    sql = "DELETE FROM series_genres WHERE series_id = ?"
    db.execute(sql, [series_id])
    sql = "DELETE FROM reviews WHERE series_id = ?"
    db.execute(sql, [series_id])
    sql = "DELETE FROM series WHERE id = ?"
    db.execute(sql, [series_id])

def get_series(series_id):
    sql = """SELECT s.id, s.title, s.description, s.year, s.episodes, s.user_id, u.username
             FROM series s JOIN users u ON u.id = s.user_id
             WHERE s.id = ?"""
    return db.query(sql, [series_id])

def get_series_genres(series_id):
    sql = """SELECT g.id, g.name
             FROM genres g JOIN series_genres sg ON sg.genre_id = g.id
             WHERE sg.series_id = ?
             ORDER BY g.name"""
    return db.query(sql, [series_id])

def get_all_series():
    sql = """SELECT id, title, year
             FROM series
             ORDER BY created_at DESC"""
    return db.query(sql)

def search_series(query):
    sql = """SELECT id, title, year, episodes
             FROM series
             WHERE title LIKE ?
             ORDER BY created_at DESC"""
    return db.query(sql, ["%" + query + "%"])

def get_all_genres():
    sql = """SELECT id, name
             FROM genres
             ORDER BY name"""
    return db.query(sql)

def get_user_review(user_id, series_id):
    sql = "SELECT id FROM reviews WHERE user_id = ? AND series_id = ?"
    return db.query(sql, [user_id, series_id])

def add_review(rating, body, user_id, series_id):
    sql = """INSERT INTO reviews (rating, body, created_at, user_id, series_id)
             VALUES (?, ?, datetime('now'), ?, ?)"""
    db.execute(sql, [rating, body, user_id, series_id])

def get_series_reviews(series_id):
    sql = """SELECT r.id, r.rating, r.body, r.created_at, r.user_id, u.username
             FROM reviews r JOIN users u ON u.id = r.user_id
             WHERE r.series_id = ?
             ORDER BY r.created_at DESC"""
    return db.query(sql, [series_id])

def get_series_rating(series_id):
    sql = """SELECT AVG(rating) AS average, COUNT(*) AS count
             FROM reviews
             WHERE series_id = ?"""
    return db.query(sql, [series_id])[0]
