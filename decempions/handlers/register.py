from flask import redirect, render_template, request, url_for
from . import auth_bp
from decempions.constants import ROUTES, HTTP_METHODS, TEMPLATES

@auth_bp.route(
	ROUTES['REGISTER'],
	methods=(HTTP_METHODS['GET'], HTTP_METHODS['POST']),
)
def register():
	if request.method == HTTP_METHODS['POST']:
		return handle_registration()
	return render_template(TEMPLATES['REGISTER'])

def handle_registration():
	print('**************')
	return redirect(url_for('/'))