# Animelist

## Features

* Users can share and browse anime series. Each series entry includes a title, description, release year, and number of episodes.
* A user can create an account and log in to the application.
* A user can add anime series and edit or delete their own entries.
* A user can view all anime series added to the application.
* A user can search for anime series by title.
* Each user has a profile page that shows statistics and the series added by that user.
* A user can assign one or more genres to a series (e.g. Action, Romance, Sci-Fi, Slice of Life).
* A user can write a review and give a rating to any series. Each series displays its reviews and average rating.

## Testing

1. Clone the repository and navigate to the project directory
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
