HTTP_METHODS = {
	'GET': 'GET',
	'POST': 'POST',
}

ROUTES = {
	'REGISTER': '/register',
	'LOGIN': '/login',
	'LOGOUT': '/logout',
	'HOME': '/home',
}

ADMIN_ROUTES = {
	'IMPORT_TEAMS': '/import-teams',
	'IMPORT_LEAGUE': '/import-league',
}

TEMPLATES = {
	'REGISTER': 'auth/register.html',
	'LOGIN': 'auth/login.html',
	'HOME': 'home.html',
}

SETTINGS = {
	'MIN_LEN': 4,
	'MAX_LEN': 50,
	'DATE_FMT': r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}$',
	'DATE_LEN': 23,
}