from . import game_bp
from flask import render_template
from decempions.auth_utils import login_required
from decempions.constants import ROUTES, TEMPLATES, HTTP_METHODS
from decempions.repositories.user_repo import UserRepository


@game_bp.route(ROUTES['RANKING'], methods=(HTTP_METHODS['GET'],))
@login_required
def ranking():
	user_repo = UserRepository()
	ranking = user_repo.get_ranking()
	return render_template(TEMPLATES['RANKING'], ranking=ranking)
