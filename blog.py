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
        ' FROM post p JOIN user u ON p.author_id = u.id'
    ).fetchall()
    return render_template('blog/index.html', posts=posts)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        artist = request.form['artist']
        genre = request.form['genre']
        length = request.form['length']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, artist, genre, length, author_id)'
                ' VALUES (?, ?, ?, ?, ?)',
                (title, artist, genre, length, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')


def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, artist, genre, author_id, length'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        artist = request.form['artist']
        genre = request.form['genre']
        length = request.form['length']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, artist = ?, genre = ?, length = ?'
                ' WHERE id = ?',
                (title, artist, genre, length, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))

#################################################################
# NAMES
@bp.route('/names/')
def names():
    db = get_db()
    unique_names = db.execute(
        'SELECT COUNT(DISTINCT artist) as count FROM post'
    )
    return render_template('names.html', posts=unique_names)


# TRACKS
@bp.route('/tracks/')
def tracks():
    db = get_db()
    tracks_number = db.execute(
        'SELECT COUNT(*) as count FROM post'
    )
    return render_template('tracks.html', posts=tracks_number)


# GENRE
@bp.route('/tracks/<genre>')
def new_genre(genre):
    db = get_db()
    genre_select = db.execute(
        f"SELECT * FROM post WHERE genre = '{genre}'",
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
            f"SELECT * FROM post WHERE genre = '{genre_insert}'",
        ).fetchall()

        return render_template('genre2.html', posts = genre_select, genres = genre_insert)

    return render_template('genre.html')


# TRACKS | SECONDS
@bp.route('/tracks-sec/')
def tracks_sec():
    db = get_db()
    tracks_number = db.execute(
        'SELECT title, length FROM post'
    ).fetchall()
    return render_template('tracks-sec.html', posts=tracks_number)


# STATISCTICS
@bp.route('/tracks-sec/statistics/')
def statistics():
    db = get_db()
    tracks_number = db.execute(
        'SELECT SUM(length) as summary, AVG(length) as middle FROM post'
    ).fetchall()
    return render_template('statistics.html', posts=tracks_number)



