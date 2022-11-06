import os

from dotenv import load_dotenv
from flask import Flask, render_template

from .database import connection
from .constants import HTTP_METHODS, ROUTES, TEMPLATES

load_dotenv()


def ensure_instance_path(app):
    try:
        os.makedirs(app.instance_path)
    except OSError:
		# already exists, it is OK
        pass


def build_server(test_config=None):
	server = Flask(__name__)
	server.config.from_mapping(
		SECRET_KEY=os.getenv('SECRET'),
		DATABASE=os.path.join(server.instance_path, os.getenv('DB_INSTANCE')),
	)

	if test_config:
		server.config.from_mapping(test_config)
	else:
		server.config.from_pyfile(os.getenv('PYFILE'), silent=True)

	ensure_instance_path(server)
	connection.init_app(server)

	@server.route(ROUTES['INDEX'], methods=[HTTP_METHODS['GET']])
	def index():
		return render_template(TEMPLATES['INDEX'])

	from . import handlers
	server.register_blueprint(handlers.auth_bp)
	server.register_blueprint(handlers.game_bp)
	server.register_blueprint(handlers.admin_bp)
	server.register_blueprint(handlers.user_bp)

	return server
