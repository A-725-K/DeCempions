import os
import click
import sqlite3

from flask import current_app, g
from flask.cli import with_appcontext

from dotenv import load_dotenv


load_dotenv()


### ---
### Utility functions
### ---
def get_db():
	if 'db' not in g:
		g.db = sqlite3.connect(
			current_app.config['DATABASE'],
			detect_types=sqlite3.PARSE_DECLTYPES
		)
		g.db.row_factory = sqlite3.Row

	return g.db


def close_db(e=None):
	db = g.pop('db', None)
	if db:
		db.close()


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


### ---
### Command line options
### ---
def init_db_handler():
	db = get_db()
	with current_app.open_resource(os.getenv('DB_FILE')) as dbfile:
		db.executescript(dbfile.read().decode())


@click.command('init-db')
@with_appcontext
def init_db_command():
	init_db_handler()
	click.echo('[!!] Database initialized')
