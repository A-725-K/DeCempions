import re

from .constants import SETTINGS
from datetime import datetime
from email_validator import validate_email, EmailNotValidError
from decempions.repositories.user_repo import UserRepository
from decempions.repositories.result_repo import ResultRepository
from decempions.repositories.match_repo import MatchRepository


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


def _get_bonus(correct_results):
	if correct_results > 9: return 100
	if correct_results > 6: return 60
	if correct_results > 4: return 30
	if correct_results > 2: return 20
	return 0


def _get_match_points(goal_home, goal_out, guess_home, guess_out, user_team):
	points = 0
	correct_guesses = 0
	correct_result = 0

	if guess_home == goal_home:
		points += 10
		correct_guesses += 1
	if guess_out == goal_out:
		points += 10
		correct_guesses += 1
	if correct_guesses == 2:
		points += 10
		correct_result = 1

	return points, correct_result


# RULES:
# 	- goal of a team ==> +10p
# 	- correct result ==> +10p
#	- goal of your team ==> +5p
#	- 3 results correct ==> +20p
#	- 5 results correct ==> +30p
#	- 7 results correct ==> +60p
#	- 10 results_correct ==> +100p
def update_players_points(week):
	user_repo = UserRepository()
	match_repo = MatchRepository()
	result_repo = ResultRepository()

	user_teams = {}
	for userteam in user_repo.get_users_favourite_teams():
		user_teams[userteam['id']] = userteam['my_team']

	matches_of_the_week = {}
	for match in match_repo.get_matches_goals_by_week(week):
		matches_of_the_week[match['id']] = match
	matches_ids = [k for k in matches_of_the_week.keys()]

	user_guesses = {}	# { user: { points, correct } }
	for guess in result_repo.get_results_by_matches_ids(matches_ids):
		match_points, correct_guess = _get_match_points(
			matches_of_the_week[guess['match_id']]['goal_home'],
			matches_of_the_week[guess['match_id']]['goal_out'],
			guess['guess_goal_home'],
			guess['guess_goal_out'],
			user_teams[guess['user_id']],
		)

		try:
			user_guesses[guess['user_id']]['points'] += match_points
		except KeyError:
			user_guesses[guess['user_id']] = {}
			user_guesses[guess['user_id']]['points'] = match_points

		try:
			user_guesses[guess['user_id']]['correct'] += correct_guess
		except KeyError:
			user_guesses[guess['user_id']]['correct'] = correct_guess

	for user_id, week_data in user_guesses.items():
		user_repo.update_user_points(
			user_id,
			week_data['points'] + _get_bonus(week_data['correct']),
		)
