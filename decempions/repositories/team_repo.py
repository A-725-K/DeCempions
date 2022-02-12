from decempions.database import connection


class TeamRepository:
	_insert_query = 'INSERT INTO Team(name) VALUES (?)'
	_find_id_by_team_name = 'SELECT id FROM Team WHERE name = ?'
	_find_team_by_id = 'SELECT name FROM Team WHERE id = ?'
	_find_teams_names_and_ids = 'SELECT id, name FROM Team'
	_update_match_result = '''
UPDATE Team
SET
	won = won + ?,
	tie = tie + ?,
	lost = lost + ?,
	goal_scored = goal_scored + ?,
	goal_conceded = goal_conceded + ?,
	points = points + ?,
	match_played = match_played + 1
WHERE id = ?
	'''
	_get_standing = '''
SELECT
	name,
	points,
	won,
	tie,
	lost,
	goal_scored,
	goal_conceded,
 	(goal_scored-goal_conceded) AS goal_diff,
	match_played
FROM Team
ORDER BY
	points DESC,
	won DESC,
	goal_scored DESC,
	goal_conceded ASC,
	goal_diff ASC
'''

	def create_team(self, team_name):
		db = connection.get_db()
		try:
			db.execute(self._insert_query, (team_name,))
			db.commit()
		except db.IntegrityError as e:
			print(str(e))
			return f'Team {team_name} already exists'

		return None


	def find_id_by_team_name(self, team_name):
		db = connection.get_db()
		row = db.execute(self._find_id_by_team_name, (team_name,)).fetchone()
		return row['id']


	def update_match_result(self, id, won, tie, lost, scored, conceded, points):
		db = connection.get_db()
		try:
			db.execute(
				self._update_match_result,
				(won, tie, lost, scored, conceded, points, id,)
			)
			db.commit()
		except Exception as e:
			print(str(e))
			return 'Error in updating team stats'

		return None


	def get_standing(self):
		db = connection.get_db()
		rows = db.execute(self._get_standing).fetchall()
		return rows


	def find_teams_names_and_ids(self):
		db = connection.get_db()
		rows = db.execute(self._find_teams_names_and_ids).fetchall()
		return rows


	def find_team_by_id(self, id):
		db = connection.get_db()
		row = db.execute(self._find_team_by_id, (id,)).fetchone()
		return row['name']
