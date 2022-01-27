from datetime import datetime

from decempions.constants import SETTINGS
from decempions.database import connection
from .team_repo import TeamRepository

class MatchRepository:
	_insert_query = '''
INSERT INTO Match(week, match_date, home_team, out_team) VALUES (?, ?, ?, ?)
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
