from . import admin_bp
from decempions.json_utils import check_int, check_str
from decempions.auth_utils import is_admin_request
from decempions.constants import ADMIN_ROUTES, HTTP_METHODS, SETTINGS
from decempions.repositories.match_repo import MatchRepository
from decempions.repositories.team_repo import TeamRepository
from flask import abort, jsonify, make_response, request


def _validate_result(result):
	err = check_str(result, 'home_team')
	if err is not None: return err

	err = check_str(result, 'out_team')
	if err is not None: return err

	err = check_int(result, 'goal_home', SETTINGS['MIN_GOAL'])
	if err is not None: return err

	err = check_int(result, 'goal_out', SETTINGS['MIN_GOAL'])
	if err is not None: return err

	return None


@admin_bp.route(
	ADMIN_ROUTES['IMPORT_WEEK_RESULTS'],
	methods=(HTTP_METHODS['POST'],)
)
@is_admin_request
def import_week_results():
	_bool_to_int = lambda cond: 1 if cond else 0
	_add_points = lambda sq1, sq2: 3 if sq1 > sq2 else 1 if sq1 == sq2 else 0

	try:
		data = request.get_json()

		err = check_int(data, 'week')
		if err is not None: raise Exception(err)

		match_repo = MatchRepository()
		team_repo = TeamRepository()

		for result in data['results']:
			err = _validate_result(result)
			if err is not None: raise Exception(err)

			home_team_id = team_repo.find_id_by_team_name(result['home_team'])
			if home_team_id is None: raise Exception('Home team not found')
			out_team_id = team_repo.find_id_by_team_name(result['out_team'])
			if out_team_id is None: raise Exception('Out team not found')

			goal_home = result.get('goal_home')
			goal_out = result.get('goal_out')
			res_str = f'{goal_home}-{goal_out}'

			err = team_repo.update_match_result(
				home_team_id,
				_bool_to_int(goal_home > goal_out),
				_bool_to_int(goal_home == goal_out),
				_bool_to_int(goal_home < goal_out),
				goal_home,
				goal_out,
				_add_points(goal_home, goal_out),
			)
			if err is not None: raise Exception(err)

			err = team_repo.update_match_result(
				out_team_id,
				_bool_to_int(goal_out > goal_home),
				_bool_to_int(goal_out == goal_home),
				_bool_to_int(goal_out < goal_home),
				goal_out,
				goal_home,
				_add_points(goal_out, goal_home),
			)
			if err is not None: raise Exception(err)

			match_id = match_repo.get_match_id_by_week_and_teams(
				data['week'],
				home_team_id,
				out_team_id,
			)
			if match_id is None: raise Exception('Match not found')

			err = match_repo.set_result(match_id, goal_home, goal_out, res_str)
			if err is not None: raise Exception(err)

	except Exception as ex:
		abort(400, description=f'Error: {str(ex)}')

	return make_response(jsonify('OK'), 200)
