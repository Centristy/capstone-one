DROP DATABASE hanguldex;
CREATE DATABASE hanguldex;

\c hanguldex


CREATE TABLE users
(
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL,
    image_url TEXT,
    header_image_url TEXT
);


CREATE TABLE decks
(
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    cover_img TEXT,
    user_id INTEGER NOT NULL REFERENCES users(id)
);


CREATE TABLE cards
(
    id SERIAL PRIMARY KEY,
    english TEXT NOT NULL,
    korean TEXT NOT NULL,
    image_url TEXT NOT NULL,
    deck_id INTEGER NOT NULL REFERENCES decks(id),
    user_id INTEGER NOT NULL REFERENCES users(id)
);
