import random
import sqlite3

db = sqlite3.connect("database.db")

db.execute("DELETE FROM reviews")
db.execute("DELETE FROM series_genres")
db.execute("DELETE FROM series")
db.execute("DELETE FROM users")

USER_COUNT = 1000
SERIES_COUNT = 10**5
REVIEW_COUNT = 10**6

for i in range(1, USER_COUNT + 1):
    db.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)",
               ["user" + str(i), "x"])

for i in range(1, SERIES_COUNT + 1):
    user_id = random.randint(1, USER_COUNT)
    db.execute("""INSERT INTO series (title, description, year, episodes, user_id, created_at)
                  VALUES (?, ?, ?, ?, ?, datetime('now'))""",
               ["series" + str(i), "description", 2000, 12, user_id])

for i in range(1, REVIEW_COUNT + 1):
    user_id = random.randint(1, USER_COUNT)
    series_id = random.randint(1, SERIES_COUNT)
    rating = random.randint(1, 5)
    db.execute("""INSERT INTO reviews (rating, body, created_at, user_id, series_id)
                  VALUES (?, ?, datetime('now'), ?, ?)""",
               [rating, "review" + str(i), user_id, series_id])

db.commit()
db.close()
