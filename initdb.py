# FLASK_APP=__init__.py flask initdb

import click

from . import create_app, db
from .models import User

from flask import Flask
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

def init_app(app):
    #app.teardown_appcontext(close_db)
    app.cli.add_command(initdb_command)

def init_db():
    appl = create_app()
    with appl.app_context():
        try:
            db.session.execute('DROP TABLE %s'%(User.__table__.name))
            db.session.commit()
            db.create_all(app=appl)
            print('Success!')
        except Exception as e:
            db.create_all(app=appl)
            print('Failed to upload to ftp: '+ str(e))
            print('Ok... :/')

@click.command('initdb')
@with_appcontext
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')