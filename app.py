from flask import (Flask, g, render_template, flash, redirect, url_for)

import models


DEBUG = True
PORT = 8000
HOST = '0.0.0.0'

app = Flask(__name__)


@app.before_request
def before_request():
    g.database = models.DATABASE
    g.database.connect()


@app.after_request
def after_request(response):
    g.database.close()
    # TODO: do I need this?
    return response


@app.route('/')
@app.route('/entries')
def index():
    return render_template('index.html')


@app.route('/entries/new')
def new():
    pass


@app.route('/entries/<id>')
def detail():
    pass


@app.route('/entries/<id>/edit')
def edit():
    pass


@app.route('/entries/<id>/delete')
def delete():
    pass


if __name__ == '__main__':
    models.initialize()
    try:
        models.Journal.create_journal(
            title='Test title',
            date=models.Journal.date,
            time_spent=5,
            learned='Learned about Flask...',
            resources='Treehouse and stackoverflow...'
        )
    except ValueError:
        pass
    app.run(debug=DEBUG, port=PORT, host=HOST)
