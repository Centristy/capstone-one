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


DROP TABLE IF EXISTS cards;
CREATE TABLE cards
(
    id SERIAL PRIMARY KEY,
    english TEXT NOT NULL,
    Korean TEXT NOT NULL,
    deck_id INTEGER NOT NULL REFERENCES decks(id)
);

DROP TABLE IF EXISTS deck_cards;
CREATE TABLE deck_cards
(
    id SERIAL PRIMARY KEY,
    deck_id INTEGER NOT NULL REFERENCES decks(id)
    card_id INTEGER NOT NULL REFERENCES cards(id)
);

