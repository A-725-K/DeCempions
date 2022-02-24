from datetime import datetime

from decempions.database import connection
from .team_repo import TeamRepository


class MatchRepository:
	_insert_query = '''
INSERT INTO Match(week, match_date, home_team, out_team) VALUES (?, ?, ?, ?)
	'''
	_get_match_id_by_week_and_teams = '''
SELECT id FROM Match WHERE week = ? AND home_team = ? AND out_team = ?
	'''
	_set_result = '''
UPDATE Match SET goal_home = ?, goal_out = ?, result = ? WHERE id = ?
	'''
	_get_league = '''
SELECT ht.name AS homeT, ot.name as outT, match_date, goal_home, goal_out, week
FROM Match
JOIN Team ht ON home_team = ht.id
JOIN Team ot ON out_team = ot.id
ORDER BY week DESC
	'''
	_get_next_week = '''
SELECT DISTINCT week
FROM Match
WHERE match_date >= CURRENT_DATE
ORDER BY week ASC
LIMIT 1
	'''
	_get_matches_by_week = '''
SELECT m.id, week, ht.name AS home_name, ot.name AS out_name, result
FROM Match AS m
JOIN Team ht ON home_team = ht.id
JOIN Team ot ON out_team = ot.id
WHERE week = ?
	'''

	def create_match(self, match):
		db = connection.get_db()

		team_repo = TeamRepository()
		home_team_id = team_repo.find_id_by_team_name(match['home_team'])
		if home_team_id is None: return 'Home team not found'
		out_team_id = team_repo.find_id_by_team_name(match['out_team'])
		if out_team_id is None: return 'Out team not found'

		fmt_date = datetime.fromisoformat(match['match_date'])

		try:
			db.execute(
				self._insert_query,
				(match['week'], fmt_date, home_team_id, out_team_id),
			)
			db.commit()
		except db.IntegrityError as e:
			print(str(e))
			return 'This match already exists'

		return None


	def get_match_id_by_week_and_teams(self, week, home_id, out_id):
		db = connection.get_db()
		row = db.execute(
			self._get_match_id_by_week_and_teams,
			(week, home_id, out_id,)
		).fetchone()
		return row['id']


	def set_result(self, match_id, goal_home, goal_out, result):
		db = connection.get_db()

		try:
			db.execute(
				self._set_result,
				(goal_home, goal_out, result, match_id),
			)
			db.commit()
		except Exception as e:
			print(str(e))
			return 'Error in setting the result of the match'

		return None


	def get_league(self):
		db = connection.get_db()
		return db.execute(self._get_league).fetchall()


	def get_next_week(self):
		db = connection.get_db()
		row = db.execute(self._get_next_week).fetchone()
		return row['week']


	def get_next_matches(self):
		db = connection.get_db()
		next_week = self.get_next_week()
		return db.execute(self._get_matches_by_week, (next_week,)).fetchall()
