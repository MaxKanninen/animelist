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