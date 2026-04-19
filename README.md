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
