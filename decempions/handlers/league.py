from . import game_bp
from flask import render_template
from decempions.auth_utils import login_required
from decempions.constants import ROUTES, TEMPLATES, HTTP_METHODS
from decempions.repositories.match_repo import MatchRepository


@game_bp.route(ROUTES['LEAGUE'], methods=(HTTP_METHODS['GET'],))
@login_required
def league():
	match_repo = MatchRepository()
	league = match_repo.get_league()
	next_week = match_repo.get_next_week()
	return render_template(
		TEMPLATES['LEAGUE'],
		league=league,
		next_week=next_week,
	)
