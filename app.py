from datetime import time
from flask import (Flask, g, render_template, flash, redirect, url_for)
from flask_bcrypt import generate_password_hash

import os

from peewee import IntegrityError
import models
import forms


DEBUG = True
PORT = 8000
HOST = '0.0.0.0'
SECRET = os.urandom(24).hex()

app = Flask(__name__)
app.secret_key = generate_password_hash(SECRET)

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
    """Index route/view, renders all titles and dates from all journal entries."""
    entries = models.Journal.select()
    return render_template('index.html', entries=entries)


@app.route('/entries')
def entries():
    """Entries route/view, redirects to index view."""
    return redirect(url_for('index'))


@app.route('/entries/new', methods=('GET', 'POST'))
def add():
    """Adding journal entry to the database and view."""
    form = forms.AddEntryForm()
    if form.validate_on_submit():
        models.Journal.create_journal(
            title=form.journal_title.data,
            date=form.journal_date.data,
            time_spent=form.journal_time_spent.data,
            learned=form.journal_learned.data,
            resources=form.journal_resources.data
        )
        flash('New journal entry has been created!', 'success')
        return redirect(url_for('index'))
    return render_template('new.html', form=form)


@app.route('/entries/<int:id>')
def detail(id):
    """Detail route/view. Displays every information about the given entry."""
    try:
        entry = models.Journal.select().where(
            models.Journal.id == id
            ).get()
    except models.DoesNotExist:
        return redirect(url_for('index'))
    return render_template('detail.html', entry=entry)


@app.route('/entries/<id>/edit')
def edit():
    pass

@app.route('/entries/<id>/delete')
def delete():
    pass


if __name__ == '__main__':
    models.initialize()
    
    # creating a test entry
    try:
        models.Journal.create_journal(
            title='Test title',
            time_spent=5,
            learned='Learned about Flask...',
            resources='Treehouse and stackoverflow...'
        )
    except ValueError:
        pass

    app.run(debug=DEBUG, port=PORT, host=HOST)
