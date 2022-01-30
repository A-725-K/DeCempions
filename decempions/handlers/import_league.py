import re
import json

from . import admin_bp
from decempions.json_utils import check_int, check_str, check_date
from decempions.auth_utils import is_admin_request
from decempions.constants import ADMIN_ROUTES, HTTP_METHODS, SETTINGS
from decempions.repositories.match_repo import MatchRepository
from flask import abort, jsonify, make_response, request


def _validate_match(match):
	err = check_int(match, 'week')
	if err is not None: return err

	err = check_str(match, 'home_team')
	if err is not None: return err

	err = check_str(match, 'out_team')
	if err is not None: return err

	err = check_date(match, 'match_date')
	if err is not None: return err

	return None


@admin_bp.route(ADMIN_ROUTES['IMPORT_LEAGUE'], methods=(HTTP_METHODS['POST'],))
@is_admin_request
def import_league():
	try:
		data = request.get_json()

		match_repo = MatchRepository()
		for match in data:
			err = _validate_match(match)
			if err is not None: raise Exception(err)
			err = match_repo.create_match(match)
			if err is not None: raise Exception(err)

	except Exception as ex:
		abort(400, description=f'Error: {str(ex)}')

	return make_response(jsonify('OK'), 200)
