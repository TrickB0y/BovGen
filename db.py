import sqlite3
from datetime import datetime

import click
from flask import current_app, g

from werkzeug.security import generate_password_hash

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
    
    if db is not None:
        db.close()
        

def init_db():
    db = get_db()
    
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))
        

@click.command('init-db')
def init_db_command():
    init_db()
    click.echo('Database inicializada.')
    
@click.command('add-user')
def addUser():
    login = input("login do usuario: ")
    password = input("senha do usuario: ")
    error = None
    
    db = get_db()
    try:
        db.execute(
            "INSERT INTO Users (login, password) VALUES (?, ?)",
            (login, generate_password_hash(password)),
        )
        db.commit()
    except db.IntegrityError:
        print(f"O Login {login} já esta cadastrado.")
    else:
        print("novo usuario adicionado.")
    
    
    
sqlite3.register_converter(
    "timestamp", lambda v: datetime.fromisoformat(v.decode())
)


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(addUser)