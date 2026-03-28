CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE series (
    id INTEGER PRIMARY KEY,
    title TEXT,
    description TEXT,
    year INTEGER,
    episodes INTEGER,
    user_id INTEGER REFERENCES users,
    created_at TEXT
);