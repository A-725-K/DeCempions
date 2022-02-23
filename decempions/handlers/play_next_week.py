from . import game_bp
from flask import flash, render_template, request
from decempions.auth_utils import login_required
from decempions.constants import ROUTES, TEMPLATES, HTTP_METHODS
from decempions.repositories.match_repo import MatchRepository


@game_bp.route(
	ROUTES['PLAY_NEXT_WEEK'],
	methods=(HTTP_METHODS['GET'], HTTP_METHODS['POST']),
)
@login_required
def play_next_week():
	match_repo = MatchRepository()
	matches = match_repo.get_next_matches()
	matches_ids = [m['id'] for m in matches]
	print(matches_ids)

	if request.method == HTTP_METHODS['POST']:
		err = handle_play_next_week()
		if err: flash(err)
		return render_template(TEMPLATES['PLAY_NEXT_WEEK'], matches=matches)

	return render_template(TEMPLATES['PLAY_NEXT_WEEK'], matches=matches)

## TODO:
##  - implement result repository
##  - validate each result written by the user (number, required)
##  - insert them in the result table
##  - improve get_next_week
##  - move styling to CSS file
##  - implement the assignment of points to players after weekly upload
def handle_play_next_week():
	return None
