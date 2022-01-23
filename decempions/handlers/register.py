import re

from . import auth_bp
from flask import flash, redirect, render_template, request, session, url_for
from decempions.constants import ROUTES, HTTP_METHODS, TEMPLATES, SETTINGS
from decempions.repositories.user_repo import UserRepository
from email_validator import validate_email, EmailNotValidError


@auth_bp.route(
	ROUTES['REGISTER'],
	methods=(HTTP_METHODS['GET'], HTTP_METHODS['POST']),
)
def register():
	if request.method == HTTP_METHODS['POST']:
		err = handle_registration()
		if err:
			flash(err)
			return render_template(TEMPLATES['REGISTER'])

		return redirect(url_for('hello'))

	return render_template(TEMPLATES['REGISTER'])


def check_username(username):
	if not username: return 'Username is required'
	username_len = len(username)
	if username_len < SETTINGS['MIN_LEN']:
		return f'Username should have at least {SETTINGS["MIN_LEN"]} characters'
	if username_len > SETTINGS['MAX_LEN']:
		return f'Username should have at most {SETTINGS["MAX_LEN"]} characters'
	if not re.match('^\w$', username):
		return 'Username must contain only letters and numbers'

	return None


def check_passwords(password, repeat_password):
	if not password: return 'Password is required'
	if not repeat_password: return 'You need to type again the password'
	if password != repeat_password: return 'You entered two different passwords'
	format_err = '''
The password should be at least 5 characters long, contains at least one
uppercase character, one lowercase character, one digit, and one character
among -_?^%&/$£!+*[]{}.,;:@|
	'''

	if len(password) < SETTINGS['MIN_LEN']: return format_err
	if not re.search('[a-z]', password): return format_err
	if not re.search('[A-Z]', password): return format_err
	if not re.search('\d', password): return format_err
	if not re.search('[-_?^%&/$£!+*\[\]{}.,;:@|]', password): return format_err

	return None


def check_email(email):
	if not email: return 'Email is required'
	try:
  		sanitized_email_addr = validate_email(email)
	except EmailNotValidError as e:
		print(str(e))
		return None, 'Email address is not valid'

	return sanitized_email_addr.email, None


def check_name(name, field):
	if not re.match('[a-zA-Z]+', name):
		return f'{field} is not a valid name'
	return None


def handle_registration():
	username = request.form.get('username')
	password = request.form.get('password')
	repeat_password = request.form.get('repeat_password')
	email = request.form.get('email')
	first_name = request.form.get('first_name')
	last_name = request.form.get('last_name')

	err = check_username(username)
	if err: return err
	err = check_passwords(password, repeat_password)
	if err: return err
	email, err = check_email(email)
	if err: return err
	err = check_name(first_name, 'First name')
	if err: return err
	err = check_name(first_name, 'Last name')
	if err: return err

	user_repo = UserRepository()
	err = user_repo.create_user(username, password, email, first_name, last_name)

	if err: return err

	return None
