from . import user_bp
from datetime import datetime
from decempions.auth_utils import login_required
from decempions.repositories.user_repo import UserRepository
from decempions.repositories.team_repo import TeamRepository
from decempions.user_utils import check_name, check_dob, check_team
from decempions.constants import (
	MONTHS, ROUTES, HTTP_METHODS, SETTINGS, TEMPLATES
)
from flask import (
	abort, g, flash, jsonify, make_response, render_template, redirect,
	request, url_for,
)

find_team = lambda t_id, tt: [team for team in tt if team['id'] == t_id][0]

@user_bp.route(
	ROUTES['EDIT'],
	methods=(HTTP_METHODS['GET'], HTTP_METHODS['POST']),
)
@login_required
def edit():
	user_repo = UserRepository()
	user = user_repo.find_user_by_username(g.username, all_fields=True)
	team_repo = TeamRepository()
	teams = team_repo.find_teams_names_and_ids()
	curr_year = datetime.now().year

	if request.method == HTTP_METHODS['POST']:
		err = handle_post(user, team_repo, user_repo)
		if err:
			flash(err)
		return redirect(url_for('user.edit'))

	return render_template(
		TEMPLATES['USER_EDIT'],
		user=user,
		year=curr_year,
		teams=teams,
		months=MONTHS,
		user_team=find_team(user['my_team'], teams)['name']
	)


def handle_post(user, team_repo, user_repo):
	first_name = request.form['first_name']
	last_name = request.form['last_name']
	day = request.form['day']
	month = request.form['month']
	year = request.form['year']
	team = request.form['my_team']

	err = check_name(first_name, 'First name')
	if err: return err
	err = check_name(first_name, 'Last name')
	if err: return err
	err = check_dob(day, month, year)
	if err: return err
	err = check_team(team, team_repo)
	if err: return err

	try:
		day = int(day)
		month = int(month)
		year = int(year)
		dob = datetime.strptime(f'{year}-{month}-{day}', SETTINGS['DOB_FMT'])
	except:
		dob = None

	try:
		team = int(team)
	except:
		team = None

	user_repo.update_user(user['id'], first_name, last_name, dob, team)

	return None
