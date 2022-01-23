-- * -- * -- * -- * -- * -- * -- * -- * -- * -- * -- * --
DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Team;
DROP TABLE IF EXISTS Match;

DROP INDEX IF EXISTS user_username_idx;
DROP INDEX IF EXISTS user_email_idx;
DROP INDEX IF EXISTS user_points_idx;
DROP INDEX IF EXISTS team_points_idx;
DROP INDEX IF EXISTS team_results_idx;
DROP INDEX IF EXISTS match_week_idx;
DROP INDEX IF EXISTS result_user_idx;
-- * -- * -- * -- * -- * -- * -- * -- * -- * -- * -- * --

-- * -- * -- * -- * -- * -- * -- * -- * -- * -- * -- * --
CREATE TABLE IF NOT EXISTS User (
	id 						INTEGER PRIMARY KEY AUTOINCREMENT,
	username 			TEXT UNIQUE NOT NULL,
	password 			TEXT NOT NULL,
	email 				TEXT UNIQUE NOT NULL,
	first_name 		TEXT,
	last_name 		TEXT,
	points 				INTEGER NOT NULL DEFAULT 0,
	next_match 		INTEGER NOT NULL DEFAULT 0,
	match_played 	INTEGER NOT NULL DEFAULT 0,
	-- pennant 		TEXT, -- path to the picture
 	created_at 		TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE UNIQUE INDEX IF NOT EXISTS user_username_idx ON User(username);
CREATE UNIQUE INDEX IF NOT EXISTS user_email_idx 		ON User(email);
CREATE 				INDEX IF NOT EXISTS user_points_idx 	ON User(points);
-- * -- * -- * -- * -- * -- * -- * -- * -- * -- * -- * --

-- * -- * -- * -- * -- * -- * -- * -- * -- * -- * -- * --
CREATE TABLE IF NOT EXISTS Team (
	id 							INTEGER PRIMARY KEY AUTOINCREMENT,
	name 						TEXT UNIQUE NOT NULL,
	points 					INTEGER NOT NULL DEFAULT 0,
	match_played 		INTEGER NOT NULL DEFAULT 0,
	won 						INTEGER NOT NULL DEFAULT 0,
	tie 						INTEGER NOT NULL DEFAULT 0,
	lost 						INTEGER NOT NULL DEFAULT 0,
	goal_scored 		INTEGER NOT NULL DEFAULT 0,
	goal_conceded 	INTEGER NOT NULL DEFAULT 0,
	created_at 			TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS team_points_idx 	ON Team(points);
CREATE INDEX IF NOT EXISTS team_results_idx ON Team(
		won, tie, lost, goal_scored, goal_conceded
);
-- * -- * -- * -- * -- * -- * -- * -- * -- * -- * -- * --

-- * -- * -- * -- * -- * -- * -- * -- * -- * -- * -- * --
CREATE TABLE IF NOT EXISTS Match (
	id 					INTEGER PRIMARY KEY AUTOINCREMENT,
	week 				INTEGER NOT NULL,
	goal_home 	INTEGER NOT NULL,
	goal_out 		INTEGER NOT NULL,
	date 				TIMESTAMP NOT NULL,
	result 			TEXT NOT NULL,
	home_team 	INTEGER NOT NULL,
	out_team 		INTEGER NOT NULL,
	created_at 	TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

	FOREIGN KEY(home_team) REFERENCES Team ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY(out_team)  REFERENCES Team ON UPDATE CASCADE ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS match_week_idx ON Match(week);
-- * -- * -- * -- * -- * -- * -- * -- * -- * -- * -- * --

-- * -- * -- * -- * -- * -- * -- * -- * -- * -- * -- * --
CREATE TABLE IF NOT EXISTS Result (
	user_id 				INTEGER NOT NULL,
	match_id				INTEGER NOT NULL,
	result					TEXT NOT NULL,
	guess_goal_home	INTEGER NOT NULL,
	guess_goal_out	INTEGER NOT NULL,
	created_at 			TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

	FOREIGN KEY(user_id) 	REFERENCES User 	ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY(match_id) REFERENCES Match 	ON UPDATE CASCADE ON DELETE CASCADE,
	PRIMARY KEY(user_id, match_id)
);
CREATE INDEX IF NOT EXISTS result_user_idx ON Result(user_id);
-- * -- * -- * -- * -- * -- * -- * -- * -- * -- * -- * --
