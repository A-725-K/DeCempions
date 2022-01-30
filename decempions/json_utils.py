from .constants import SETTINGS

def check_str(dic, key):
	string = dic.get(key)
	if string is not None and type(string) is str:
		s_len = len(string)
		if s_len < SETTINGS['MIN_LEN'] or s_len > SETTINGS['MAX_LEN']:
			return f'{key} is not in the correct format'
	else: return f'{key} has not the correct type'
	return None


def check_date(dic, key):
	date = dic.get(key)
	if date is not None and type(date) is str:
		if len(date) != SETTINGS['DATE_LEN']:
			return f'{key} has a wrong length'
		if not re.match(SETTINGS['DATE_FMT'], date):
			return f'{key} is not in the correct format'
	else: return f'{key} has not the correct type'
	return None


def check_int(dic, key):
	i = dic.get(key)
	if i is None or type(i) is not int or i < 1:
		return f'{key} is not in the correct format'
	return None