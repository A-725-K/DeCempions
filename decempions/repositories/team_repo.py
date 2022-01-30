from decempions.database import connection

class TeamRepository:
	_insert_query = 'INSERT INTO Team(name) VALUES (?)'
	_find_id_by_team_name = 'SELECT id FROM Team WHERE name = ?'
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
# 	_get_standing = '''
# SELECT name, points, won, goal_scored, (goal_scored-goal_conceded) AS goal_diff
# FROM Team
# ORDER BY points, won, goal_scored, goal_diff DESC
# '''

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
