from decempions.database import connection
from werkzeug.security import generate_password_hash


class UserRepository:
	_insert_query = '''
INSERT INTO User(username, password, email, first_name, last_name)
VALUES (?, ?, ?, ?, ?)
	'''
	_find_by_username = 'SELECT username, password FROM User WHERE username = ?'
	_find_by_username_all = 'SELECT * FROM User WHERE username = ?'
	_find_by_email = 'SELECT username, password FROM User WHERE email = ?'
	_find_admin_by_token = 'SELECT is_admin FROM User WHERE token = ?'
	_update_user = '''
UPDATE User
SET
	first_name = ?,
	last_name = ?,
	date_of_birth = ?,
	my_team = ?
WHERE id = ?
'''

	def create_user(self, username, password, email, first_name, last_name):
		db = connection.get_db()
		try:
			db.execute(
				self._insert_query,
				(username, generate_password_hash(password), email,
				first_name, last_name,)
			)
			db.commit()
		except db.IntegrityError as e:
			print(str(e))
			return f'Username {username} already exists'

		return None


	def find_user_by_username(self, username, all_fields=False):
		db = connection.get_db()
		if not all_fields:
			return db.execute(self._find_by_username, (username,)).fetchone()
		return db.execute(self._find_by_username_all, (username,)).fetchone()


	def find_user_by_email(self, email):
		db = connection.get_db()
		return db.execute(self._find_by_email, (email,)).fetchone()


	def find_admin_by_token(self, token):
		db = connection.get_db()
		return db.execute(self._find_admin_by_token, (token,)).fetchone()


	def update_user(self, id, first_name, last_name, dob, team):
		db = connection.get_db()
		try:
			db.execute(
				self._update_user,
				(first_name, last_name, dob, team, id,)
			)
			db.commit()
		except db.IntegrityError as e:
			print(str(e))
			return f'Cannot update user'

		return None
