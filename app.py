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
    return response


@app.route('/')
def index():
    entries = models.Journal.select()
    return render_template('index.html', entries=entries)


@app.route('/entries')
def entries():
    return redirect(url_for('index'))


@app.route('/entries/new')
def new():
    pass


@app.route('/entries/<int:id>')
def detail(id):
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
