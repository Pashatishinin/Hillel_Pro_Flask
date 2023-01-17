import sqlite3
import json
import click
from flask import current_app, g


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
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(add_fixtures)



@click.command('fixtures')
def add_fixtures():
    """Clear the existing data and create new tables."""
    load_fixtures()
    click.echo('All fixtures in database.')


def load_fixtures():
    db = get_db()
    with open("fixtures.json", "r") as json_file:
        fixture: dict = json.load(json_file)
        for a in fixture.values():
            db.execute(
                'INSERT INTO tracks (title, artist, genre, length)'
                ' VALUES (?, ?, ?, ?)',
                (a.get('title'), a.get('artist'), a.get('genre'), a.get('length'),))
    db.commit()




