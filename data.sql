DROP DATABASE IF EXISTS  hanguldex;
CREATE DATABASE hanguldex;

\c hanguldex

DROP TABLE IF EXISTS users;
CREATE TABLE users
(
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL,
    image_url TEXT,
    header_image_url TEXT
);

DROP TABLE IF EXISTS decks;
CREATE TABLE decks
(
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    cover_img TEXT,
    user_id INTEGER NOT NULL REFERENCES users(id)
);