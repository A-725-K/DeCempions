from . import game_bp
from flask import render_template
from decempions.auth_utils import login_required
from decempions.constants import ROUTES, TEMPLATES, HTTP_METHODS
from decempions.repositories.team_repo import TeamRepository


@game_bp.route(ROUTES['STANDING'], methods=(HTTP_METHODS['GET'],))
@login_required
def standings():
	team_repo = TeamRepository()
	standing = team_repo.get_standing()
	return render_template(TEMPLATES['STANDING'], standing=standing)
