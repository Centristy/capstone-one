DROP DATABASE IF EXISTS  hanguldex;
CREATE DATABASE hanguldex;

\c hanguldex

DROP TABLE IF EXISTS users;
CREATE TABLE users
(
    username Text PRIMARY KEY,
    email Text NOT NULL,
    password TEXT NOT NULL,
    image_url TEXT
);