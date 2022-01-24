from . import game_bp
from flask import render_template
from decempions.auth_utils import login_required
from decempions.constants import ROUTES, TEMPLATES

@game_bp.route(ROUTES['HOME'])
@login_required
def home():
	return render_template(TEMPLATES['HOME'])
