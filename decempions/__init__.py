import os

from flask import Flask
from dotenv import load_dotenv

from .database import connection

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

	@server.route('/hello')
	def hello():
		return '<h1 style="color: red; background-color: yellow;">Hello!</h1>'

	from . import handlers
	server.register_blueprint(handlers.auth_bp)

	return server
