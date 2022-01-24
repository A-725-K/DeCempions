from . import auth_bp
from flask import flash, redirect, render_template, request, session, url_for
from decempions.repositories.user_repo import UserRepository
from decempions.constants import ROUTES, HTTP_METHODS, TEMPLATES
from werkzeug.security import check_password_hash


@auth_bp.route(
	ROUTES['LOGIN'],
	methods=(HTTP_METHODS['GET'], HTTP_METHODS['POST']),
)
def login():
	if request.method == HTTP_METHODS['POST']:
		err = handle_login()
		if err:
			flash(err)
			return render_template(TEMPLATES['LOGIN'])

		return redirect(url_for('game.home'))

	return render_template(TEMPLATES['LOGIN'])


def handle_login():
	username = request.form.get('username')
	password = request.form.get('password')

	if not username or not password: return 'Username and password are required'

	user_repo = UserRepository()
	user = user_repo.find_user_by_username(username)
	print('---- [PASSWORD in User]', user['password'])
	print('---- [PASSWORD in form]', password)
	print('---- [PASSWORD check]', check_password_hash(password, user['password']))
	print('---- [PASSWORD check]', check_password_hash(user['password'], password))
	if not user or not check_password_hash(user['password'], password):
		return 'Username or password are not correct'

	session.clear()
	session['username'] = user['username']
	return None

