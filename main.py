import os


from flask import Flask, render_template, request

from db import get_db


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'tracks.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    import db
    db.init_app(app)

    create_views(app)

    return app


def create_views(app):

    @app.route('/')
    def index():
        db = get_db()
        posts = db.execute(
            'SELECT * FROM tracks'
        ).fetchall()
        return render_template('blog/index.html', posts=posts)

    @app.route('/names/')
    def names():
        db = get_db()
        unique_names = db.execute(
            'SELECT COUNT(DISTINCT artist) as count FROM tracks'
        )
        return render_template('names.html', posts=unique_names)

    # TRACKS
    @app.route('/tracks/')
    def tracks():
        db = get_db()
        tracks_number = db.execute(
            'SELECT COUNT(*) as count FROM tracks'
        )
        return render_template('tracks.html', posts=tracks_number)

    # GENRE
    @app.route('/tracks/<genre>')
    def new_genre(genre):
        db = get_db()
        genre_select = db.execute(
            f"SELECT * FROM tracks WHERE genre = '{genre}'",
        ).fetchall()

        return render_template('genre2.html', posts=genre_select, genres=genre)

    # GENRE VERSION 2
    @app.route('/tracks/genre', methods=('GET', 'POST'))
    def genre():
        db = get_db()
        if request.method == 'POST':
            genre_insert = request.form['genre']
            error = None

            genre_select = db.execute(
                f"SELECT * FROM tracks WHERE genre = '{genre_insert}'",
            ).fetchall()

            return render_template('genre2.html', posts=genre_select, genres=genre_insert)

        return render_template('genre.html')

    # TRACKS | SECONDS
    @app.route('/tracks-sec/')
    def tracks_sec():
        db = get_db()
        tracks_number = db.execute(
            'SELECT title, length FROM tracks'
        ).fetchall()
        return render_template('tracks-sec.html', posts=tracks_number)

    # STATISCTICS
    @app.route('/tracks-sec/statistics/')
    def statistics():
        db = get_db()
        tracks_number = db.execute(
            'SELECT SUM(length) as summary, AVG(length) as middle FROM tracks'
        ).fetchall()
        return render_template('statistics.html', posts=tracks_number)


