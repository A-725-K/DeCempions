from decempions.database import connection

class TeamRepository:
	_insert_query = 'INSERT INTO Team(name) VALUES (?)'
	_find_id_by_team_name = 'SELECT id FROM Team WHERE name = ?'
# 	_update_result = '''
# UPDATE SET
# 	? = ?+1,
# 	goal_scored = goal_scored+?,
# 	goal_conceded=goal_conceded+?
# WHERE id = ?
# 	'''

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
