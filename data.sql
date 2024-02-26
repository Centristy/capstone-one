
DROP DATABASE IF EXISTS hanguldex;
CREATE DATABASE hanguldex;

\c hanguldex


CREATE TABLE users
(
    id BIGSERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL,
    image_url TEXT,
    header_image_url TEXT
);


CREATE TABLE decks
(
    id BIGSERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    cover_img TEXT,
    user_id INT NOT NULL REFERENCES users(id)
);


CREATE TABLE cards
(
    id BIGSERIAL PRIMARY KEY,
    english TEXT NOT NULL,
    korean TEXT NOT NULL,
    image_url TEXT NOT NULL,
    deck_id INT NOT NULL REFERENCES decks(id),
    user_id INT NOT NULL REFERENCES users(id)
);
