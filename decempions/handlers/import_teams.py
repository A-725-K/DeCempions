from . import admin_bp
from decempions.auth_utils import is_admin_request
from decempions.constants import ADMIN_ROUTES, HTTP_METHODS
from decempions.repositories.team_repo import TeamRepository
from flask import abort, request


@admin_bp.route(ADMIN_ROUTES['IMPORT_TEAMS'], methods=(HTTP_METHODS['POST'],))
@is_admin_request
def import_teams():
	try:
		team_names = request.get_data().decode('utf8').split('\n')
		team_repo = TeamRepository()
		for team in team_names:
			err = team_repo.create_team(team)
			if err: raise err
	except Exception as ex:
		abort(400, description=f'Error: {ex}')

	return 'OK'