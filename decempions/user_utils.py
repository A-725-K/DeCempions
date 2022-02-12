import re

from .constants import SETTINGS
from datetime import datetime
from email_validator import validate_email, EmailNotValidError


def check_username(username):
	if not username: return 'Username is required'
	username_len = len(username)
	if username_len < SETTINGS['MIN_LEN']:
		return f'Username should have at least {SETTINGS["MIN_LEN"]} characters'
	if username_len > SETTINGS['MAX_LEN']:
		return f'Username should have at most {SETTINGS["MAX_LEN"]} characters'
	if not re.match('^\w+$', username):
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
	if not name: return None
	if not re.match('[a-zA-Z]+', name) or len(name) > SETTINGS['MAX_LEN']:
		return f'{field} is not a valid name'
	return None


def check_dob(day, month, year):
	print('---', day, month, year)
	if (day is None or day == '') and \
		(month is None or month == '') and \
		(year is None or year == ''): return None
	try:
		datetime.strptime(f'{year}-{month}-{day}', SETTINGS['DOB_FMT'])
	except ValueError:
		return 'Date is not correct'
	return None


def check_team(team_id, team_repo=None):
	if team_id is None or team_id == '': return None

	team_id = int(team_id)
	if team_id <= 0: return 'Team id is not valid'
	if team_repo is None: team_repo = TeamRepository()
	team = team_repo.find_team_by_id(team_id)
	if team is None: return 'Team not found'

	return None

