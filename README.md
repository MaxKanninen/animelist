# Animelist

Animelist is a web application for browsing and sharing anime series. Users can add series to the catalog, assign genres, and write reviews with ratings.

## Features

* A user can create an account and log in to the application.
* A user can add anime series and edit or delete their own entries. Each series has a title, description, release year, and episode count.
* A user can assign one or more genres to a series (e.g. Action, Romance, Sci-Fi, Slice of Life).
* A user can view all anime series added to the application.
* A user can search for anime series by title.
* A user can write a review and give a rating (1–5) to any series. Each series displays its reviews and average rating.
* Each user has a profile page showing statistics and the series they have added.

## Testing

1. Clone the repository and navigate to the project directory.
2. Create and activate a virtual environment:
```
python3 -m venv venv
source venv/bin/activate
```
3. Install Flask:
```
pip install flask
```
4. Initialize the database:
```
sqlite3 database.db < schema.sql
```
5. Run the application:
```
flask run
```
6. Open `http://localhost:5000` in a browser and register a new account to start using the app.

## Performance with a large dataset

The script `seed.py` fills the database with 1,000 users, 100,000 series and 1,000,000 reviews. The reviews are distributed evenly between series, so each series has on average ten reviews.

The series page runs the following query to read the reviews of one series:

```sql
SELECT r.id, r.rating, r.body, r.created_at, r.user_id, u.username
FROM reviews r JOIN users u ON u.id = r.user_id
WHERE r.series_id = ?
ORDER BY r.created_at DESC
```

Without the index `idx_reviews_series_id`, the query takes about 35 ms because the database scans the entire `reviews` table for every request:

```
Run Time: real 0.040 ...
Run Time: real 0.034 ...
Run Time: real 0.035 ...
```

After adding the index, the query finishes in under 1 ms:

```
Run Time: real 0.000 ...
Run Time: real 0.000 ...
Run Time: real 0.000 ...
```

The same speedup applies to `get_series_rating`, which also filters reviews by `series_id`. The index is defined in `schema.sql`.
