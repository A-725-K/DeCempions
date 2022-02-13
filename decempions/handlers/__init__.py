from flask import Blueprint, g, session

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
game_bp = Blueprint('game', __name__, url_prefix='/game')
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')
user_bp = Blueprint('user', __name__, url_prefix='/user')


@auth_bp.before_app_request
def load_logged_in_user():
	g.username = session.get('username')


@game_bp.before_app_request
def load_logged_in_user():
	g.username = session.get('username')


@user_bp.before_app_request
def load_logged_in_user():
	g.username = session.get('username')


from .register import *
from .login import *
from .logout import *
from .home import *
from .import_teams import *
from .import_league import *
from .import_week_results import *
from .standing import *
from .edit_user import *
from .ranking import *
