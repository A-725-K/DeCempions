HTTP_METHODS = {
	'GET': 'GET',
	'POST': 'POST',
}

ROUTES = {
	'REGISTER': '/register',
	'LOGIN': '/login',
	'LOGOUT': '/logout',
	'HOME': '/home',
	'STANDING': '/standing',
	'EDIT': '/edit',
}

ADMIN_ROUTES = {
	'IMPORT_TEAMS': '/import-teams',
	'IMPORT_LEAGUE': '/import-league',
	'IMPORT_WEEK_RESULTS': '/import-week-results',
}

TEMPLATES = {
	'REGISTER': 'auth/register.html',
	'LOGIN': 'auth/login.html',
	'HOME': 'home.html',
	'STANDING': 'game/standing.html',
	'USER_EDIT': 'profile/user.html',
}

SETTINGS = {
	'MIN_LEN': 4,
	'MAX_LEN': 50,
	'DATE_FMT': r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}$',
	'DATE_LEN': 23,
	'MIN_GOAL': 0,
	'DOB_FMT': '%Y-%m-%d',
}
