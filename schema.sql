CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL
);

CREATE TABLE series (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    year INTEGER NOT NULL,
    episodes INTEGER NOT NULL,
    user_id INTEGER NOT NULL REFERENCES users,
    created_at TEXT NOT NULL
);

CREATE TABLE genres (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE series_genres (
    series_id INTEGER NOT NULL REFERENCES series,
    genre_id INTEGER NOT NULL REFERENCES genres,
    PRIMARY KEY (series_id, genre_id)
);

CREATE TABLE reviews (
    id INTEGER PRIMARY KEY,
    rating INTEGER NOT NULL,
    body TEXT NOT NULL,
    created_at TEXT NOT NULL,
    user_id INTEGER NOT NULL REFERENCES users,
    series_id INTEGER NOT NULL REFERENCES series
);

INSERT INTO genres (name) VALUES ('Action');
INSERT INTO genres (name) VALUES ('Comedy');
INSERT INTO genres (name) VALUES ('Drama');
INSERT INTO genres (name) VALUES ('Fantasy');
INSERT INTO genres (name) VALUES ('Horror');
INSERT INTO genres (name) VALUES ('Romance');
INSERT INTO genres (name) VALUES ('Sci-Fi');
INSERT INTO genres (name) VALUES ('Slice of Life');
INSERT INTO genres (name) VALUES ('Sports');
INSERT INTO genres (name) VALUES ('Thriller');
