import db

def add_series(title, description, year, episodes, user_id):
    sql = "INSERT INTO series (title, description, year, episodes, user_id, created_at) VALUES (?, ?, ?, ?, ?, datetime('now'))"
    db.execute(sql, [title, description, year, episodes, user_id])

def edit_series(title, description, year, episodes, series_id):
    sql = """UPDATE series
             SET title = ?, description = ?, year = ?, episodes = ?
             WHERE id = ?"""
    db.execute(sql, [title, description, year, episodes, series_id])

def delete_series(series_id):
    sql = "DELETE FROM series WHERE id = ?"
    db.execute(sql, [series_id])

def get_series(series_id):
    sql = "SELECT id, title, description, year, episodes, user_id FROM series WHERE id = ?"
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