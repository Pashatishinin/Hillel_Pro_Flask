from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from auth import login_required
from db import get_db

bp = Blueprint('blog', __name__)


@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, artist, genre, length, author_id'
        ' FROM tracks p JOIN user u ON p.author_id = u.id'
    ).fetchall()
    return render_template('blog/index.html', posts=posts)

#################################################################
# NAMES
@bp.route('/names/')
def names():
    db = get_db()
    unique_names = db.execute(
        'SELECT COUNT(DISTINCT artist) as count FROM tracks'
    )
    return render_template('names.html', posts=unique_names)


# TRACKS
@bp.route('/tracks/')
def tracks():
    db = get_db()
    tracks_number = db.execute(
        'SELECT COUNT(*) as count FROM tracks'
    )
    return render_template('tracks.html', posts=tracks_number)


# GENRE
@bp.route('/tracks/<genre>')
def new_genre(genre):
    db = get_db()
    genre_select = db.execute(
        f"SELECT * FROM tracks WHERE genre = '{genre}'",
    ).fetchall()

    return render_template('genre2.html', posts=genre_select, genres=genre)


# GENRE VERSION 2
@bp.route('/tracks/genre', methods=('GET', 'POST'))
def genre():
    db = get_db()
    if request.method == 'POST':
        genre_insert = request.form['genre']
        error = None

        genre_select = db.execute(
            f"SELECT * FROM tracks WHERE genre = '{genre_insert}'",
        ).fetchall()

        return render_template('genre2.html', posts = genre_select, genres = genre_insert)

    return render_template('genre.html')


# TRACKS | SECONDS
@bp.route('/tracks-sec/')
def tracks_sec():
    db = get_db()
    tracks_number = db.execute(
        'SELECT title, length FROM tracks'
    ).fetchall()
    return render_template('tracks-sec.html', posts=tracks_number)


# STATISCTICS
@bp.route('/tracks-sec/statistics/')
def statistics():
    db = get_db()
    tracks_number = db.execute(
        'SELECT SUM(length) as summary, AVG(length) as middle FROM tracks'
    ).fetchall()
    return render_template('statistics.html', posts=tracks_number)



