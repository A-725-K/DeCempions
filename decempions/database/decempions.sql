DROP TABLE IF EXISTS Users;

CREATE TABLE IF NOT EXISTS Users (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	username TEXT UNIQUE NOT NULL,
	password TEXT NOT NULL,
	email TEXT UNIQUE NOT NULL,
	first_name TEXT,
	last_name TEXT,
 	created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
