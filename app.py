from flask import (Flask, g, render_template, flash,
                   redirect, url_for)
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_required, login_user

import os
import datetime 

import models
import forms


################################
# app config
################################
DEBUG = True
PORT = 8000
HOST = '0.0.0.0'
SECRET = os.urandom(24).hex()

app = Flask(__name__)
app.secret_key = generate_password_hash(SECRET)

################################
# login
################################
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def user(uid):
    try:
        return models.User.get(models.User.id == uid)
    except models.DoesNotExist:
        flash("User does not exist!")
        return None


@app.before_request
def before_request():
    g.database = models.DATABASE
    g.database.connect()


@app.after_request
def after_request(response):
    g.database.close()
    return response


@app.route('/login', methods=('GET', 'POST'))
def login():
    """
    Login existing user.
    Please use the test user:
    username : test_user
    password : password
    """
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.username == form.username.data)
        except models.DoesNotExist:
            flash("Username or password is wrong.", "error")
        else:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("You have logged in!")
                return redirect(url_for('index'))
            else:
                flash("Username or password is wrong.", "error")
    return render_template('login.html', form=form)


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
@login_required
def add():
    """Adding journal entry to the database and view."""
    form = forms.AddEntryForm()
    query = models.Journal.select().where(models.Journal.title == form.journal_title.data)

    if form.validate_on_submit():
        if query:
            flash('Entry with that Title already exists.')
        else:
            models.Journal.create_journal(
                title=form.journal_title.data,
                date=form.journal_date.data,
                time_spent=form.journal_time_spent.data,
                learned=form.journal_learned.data,
                resources=form.journal_resources.data
            )
            flash('New entry added successfully!', 'success')
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


@app.route('/entries/<id>/edit', methods=('GET', 'POST'))
@login_required
def edit(id):
    """Edit existing entry."""

    try:
        entry = models.Journal.select().where(
            models.Journal.id == id
        ).get()
    except models.DoesNotExist:
        return redirect(url_for('detail', entry=id))

    edit_form = forms.AddEntryForm()

    if edit_form.validate_on_submit():
        models.Journal.update(
            title=edit_form.journal_title.data,
            date=edit_form.journal_date.data,
            time_spent=edit_form.journal_time_spent.data,
            learned=edit_form.journal_learned.data,
            resources=edit_form.journal_resources.data
        ).where(models.Journal.id == id).execute()
        flash('Entry updated successfully!', 'success')
        return redirect(url_for('detail', id=id))
    return render_template('edit.html', edit_form=edit_form, entry=entry)


@app.route('/entries/<int:id>/delete', methods=('GET', 'POST'))
@login_required
def delete(id):
    """Delete existing entry."""
    try:
        entry = models.Journal.select().where(
            models.Journal.id == id
        ).get()
        with models.DATABASE.atomic():
            models.Journal.delete_by_id(entry)
            flash('Following entry was deleted: {}'.format(entry.title))
    except models.DoesNotExist:
        flash('Entry id does not exist!', 'error')
    return redirect(url_for('index'))



if __name__ == '__main__':
    models.initialize()

    models.User.create_user(
        username='test_user',
        password='password'
    )

    if models.Journal.select().count() == 0:
        models.Journal.create_journal(
            title='Hello, World! Flask edition.',
            date=datetime.datetime.now(),
            time_spent=1,
            learned='Learned some flask!',
            resources='teamtreehouse'
        )

    app.run(debug=DEBUG, port=PORT, host=HOST)
