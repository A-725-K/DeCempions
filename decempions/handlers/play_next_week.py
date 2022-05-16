from . import game_bp
from flask import abort, flash, render_template, request, session
from decempions.auth_utils import login_required
from decempions.constants import ROUTES, TEMPLATES, HTTP_METHODS
from decempions.repositories.match_repo import MatchRepository
from decempions.repositories.result_repo import ResultRepository


@game_bp.route(
	ROUTES['PLAY_NEXT_WEEK'],
	methods=(HTTP_METHODS['GET'], HTTP_METHODS['POST']),
)
@login_required
def play_next_week():
	user_id = session['user_id']
	if user_id is None: abort(500, 'Internal Server Error')

	match_repo = MatchRepository()
	result_repo = ResultRepository()

	week, matches = match_repo.get_next_matches()
	matches_ids = [m['id'] for m in matches]

	user_guess_query_res = result_repo.get_results_by_user_and_matches(
		user_id,
		matches_ids,
	)
	user_guess = {}
	for res in user_guess_query_res:
		user_guess[res['match_id']] = {
			'user_id': user_id,
			'match_id': res['match_id'],
			'guess_goal_home': res['guess_goal_home'],
			'guess_goal_out': res['guess_goal_out'],
		}

	if request.method == HTTP_METHODS['POST']:
		new_user_guess, err = handle_play_next_week(
			user_id,
			matches_ids,
			result_repo,
		)
		if err: flash(err)
		return render_template(
			TEMPLATES['PLAY_NEXT_WEEK'],
			matches=matches,
			user_guess=new_user_guess,
			week=week,
		)

	return render_template(
		TEMPLATES['PLAY_NEXT_WEEK'],
		matches=matches,
		user_guess=user_guess,
		week=week,
	)


def _check_number(n, field_name):
	try:
		n = int(n)
	except:
		return f'{field_name} is not a number'
	if n < 0: return 'A guess cannot be negative'
	return None


def handle_play_next_week(user_id, matches_ids, result_repo):
	results_to_insert = []
	guess = {}
	for match_id in matches_ids:
		guess_home_html_id = f'guess_home_{match_id}'
		guess_out_html_id = f'guess_out_{match_id}'

		guess_goal_home = request.form.get(guess_home_html_id)
		guess_goal_out = request.form.get(guess_out_html_id)

		err = _check_number(guess_goal_home, guess_home_html_id)
		if err: return None, err
		err = _check_number(guess_goal_out, guess_out_html_id)
		if err: return None, err

		guess_goal_home = int(guess_goal_home)
		guess_goal_out = int(guess_goal_out)

		new_result = {
			'user_id': user_id,
			'match_id': match_id,
			'guess_goal_home': guess_goal_home,
			'guess_goal_out': guess_goal_out,
		}
		results_to_insert.append(new_result)
		guess[match_id] = new_result

	for result_to_insert in results_to_insert:
		err = result_repo.insert_result(result_to_insert)
		if err: return None, err

	return guess, None
