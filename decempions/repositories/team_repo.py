from decempions.database import connection

class TeamRepository:
	_insert_query = 'INSERT INTO Team(name) VALUES (?)'
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
