from flask_wtf.form import FlaskForm
from wtforms.fields.core import DateField, IntegerField, StringField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired, Optional, ValidationError

from models import Journal


def entry_exist(form, field):
    if Journal.select().where(Journal.title == field.data).exists():
        raise ValidationError('Entry with that title already exists.')


class AddEntryForm(FlaskForm):
    journal_title = StringField(
        'Title',
        validators=[DataRequired(), entry_exist]
    )
    journal_date = DateField(
        'YYYY-MM-DD',
        validators=[Optional()],
        format='%Y-%m-%d'
    )
    journal_time_spent = IntegerField(
        'Time Spent',
        validators=[DataRequired()]
    )
    journal_learned = TextAreaField(
        'What I Learned',
        validators=[Optional()]
    )
    journal_resources = TextAreaField(
        'Resources to Remember',
        validators=[Optional()]
    )
