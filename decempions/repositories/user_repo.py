from decempions.database import connection
from werkzeug.security import generate_password_hash

class UserRepository():
	_insert_query = '''
INSERT INTO User(username, password, email, first_name, last_name)
VALUES (?, ?, ?, ?, ?)
	'''
	_find_by_username = 'SELECT username, password FROM User WHERE username = ?'
	_find_by_email = 'SELECT username, password FROM User WHERE email = ?'

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


	def find_user_by_username(self, username):
		db = connection.get_db()
		return db.execute(self._find_by_username, (username,)).fetchone()


	def find_user_by_email(self, email):
		db = connection.get_db()
		return db.execute(self._find_by_email, (email,)).fetchone()
