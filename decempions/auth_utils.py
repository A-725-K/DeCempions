import functools

from flask import abort, g, request, redirect, url_for
from decempions.repositories.user_repo import UserRepository

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.username is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view


def is_admin_request(view):
	@functools.wraps(view)
	def wrapped_view(**kwargs):
		token = request.headers.get('DC-Token')
		if token is None:
			abort(401, description='Not authorized')

		user_repo = UserRepository()
		if not bool(user_repo.find_admin_by_token(token)):
			abort(403, description='Forbidden')

		return view(**kwargs)
	return wrapped_view
