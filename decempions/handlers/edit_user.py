from . import user_bp
from decempions.auth_utils import login_required
from decempions.constants import ROUTES, HTTP_METHODS, TEMPLATES
from decempions.repositories.user_repo import UserRepository
from flask import (
	abort, g, flash, jsonify, make_response, render_template, request
)

@user_bp.route(
	ROUTES['EDIT'],
	methods=(HTTP_METHODS['GET'], HTTP_METHODS['POST']),
)
@login_required
def edit():
	user_repo = UserRepository()
	user = user_repo.find_user_by_username(g.username, all_fields=True)
	print(f'g.username = {g.username}\nuser = {user["username"]}')

	if request.method == HTTP_METHODS['POST']:
		err = handle_post(user)
		if err:
			flash(err)

	return render_template(TEMPLATES['USER_EDIT'], user=user)


def handle_post(user):
	first_name = request.form['first_name']
	last_name = request.form['last_name']
	day = request.form['day']
	month = request.form['month']
	year = request.form['year']

	return None
