from . import admin_bp
from decempions.json_utils import check_str
from decempions.auth_utils import is_admin_request
from decempions.constants import ADMIN_ROUTES, HTTP_METHODS
from decempions.repositories.team_repo import TeamRepository
from flask import abort, jsonify, make_response, request


@admin_bp.route(ADMIN_ROUTES['IMPORT_TEAMS'], methods=(HTTP_METHODS['POST'],))
@is_admin_request
def import_teams():
	try:
		data = request.get_json()

		team_repo = TeamRepository()
		for team in data:
			err = check_str(team)
			if err is not None: raise Exception(err)
			err = team_repo.create_team(team['team_name'])
			if err is not None: raise Exception(err)

	except Exception as ex:
		abort(400, description=f'Error: {str(ex)}')

	return make_response(jsonify('OK'), 200)