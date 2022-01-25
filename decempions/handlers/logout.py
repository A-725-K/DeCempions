from . import auth_bp
from decempions.constants import ROUTES
from flask import redirect, session, url_for


@auth_bp.route(ROUTES['LOGOUT'])
def logout():
	session.clear()
	return redirect(url_for('auth.register'))
