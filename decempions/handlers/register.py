from . import auth_bp
from flask import flash, redirect, render_template, request, session, url_for
from decempions.constants import ROUTES, HTTP_METHODS, TEMPLATES
from decempions.repositories.user_repo import UserRepository
from decempions.user_utils import (
	check_name, check_email, check_username, check_passwords,
)


@auth_bp.route(
	ROUTES['REGISTER'],
	methods=(HTTP_METHODS['GET'], HTTP_METHODS['POST']),
)
def register():
	if session.get('username'): return redirect(url_for('game.home'))

	if request.method == HTTP_METHODS['POST']:
		err, fill_values = handle_registration()
		if err:
			flash(err)
			return render_template(
				TEMPLATES['REGISTER'],
				username=fill_values.get('username'),
				email=fill_values.get('email'),
				first_name=fill_values.get('first_name'),
				last_name=fill_values.get('last_name'),
			)

		return redirect(url_for('auth.login'))

	return render_template(TEMPLATES['REGISTER'])


def handle_registration():
	fill_values = {}

	username = request.form.get('username')
	password = request.form.get('password')
	repeat_password = request.form.get('repeat_password')
	email = request.form.get('email')
	first_name = request.form.get('first_name')
	last_name = request.form.get('last_name')

	fill_values['username'] = username
	fill_values['email'] = email
	fill_values['first_name'] = first_name
	fill_values['last_name'] = last_name

	err = check_username(username)
	if err: return err, fill_values
	err = check_passwords(password, repeat_password)
	if err: return err, fill_values
	email, err = check_email(email)
	if err: return err, fill_values
	err = check_name(first_name, 'First name')
	if err: return err, fill_values
	err = check_name(first_name, 'Last name')
	if err: return err, fill_values

	user_repo = UserRepository()
	err = user_repo.create_user(username, password, email, first_name, last_name)

	if err: return err, fill_values

	return None, {}
