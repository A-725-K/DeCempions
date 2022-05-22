from decempions.database import connection


class ResultRepository:
	_insert_query = '''
INSERT INTO Result(user_id, match_id, guess_goal_home, guess_goal_out)
VALUES (?, ?, ?, ?)
	'''
	_results_by_user_and_matches = lambda _, n: f'''
SELECT match_id, guess_goal_home, guess_goal_out
FROM Result
WHERE user_id = ? AND match_id IN ({("?," * n)[:-1]})
	'''
	_results_by_matches_ids = lambda _, n: f'''
SELECT * FROM Result WHERE match_id IN ({("?," * n)[:-1]})
	'''

	def insert_result(self, result):
		db = connection.get_db()
		try:
			db.execute(
				self._insert_query,
				(
					result['user_id'], result['match_id'],
					result['guess_goal_home'], result['guess_goal_out'],
				),
			)
			db.commit()
		except db.IntegrityError as e:
			print(str(e))
			return 'This result already exists'

		return None

	def get_results_by_user_and_matches(self, user_id, matches_ids):
		db = connection.get_db()
		return db.execute(
			self._results_by_user_and_matches(len(matches_ids)),
			(user_id, *matches_ids,),
		).fetchall()

	def get_results_by_matches_ids(self, matches_ids):
		db = connection.get_db()
		return db.execute(
			self._results_by_matches_ids(len(matches_ids)),
			(*matches_ids,),
		).fetchall()
