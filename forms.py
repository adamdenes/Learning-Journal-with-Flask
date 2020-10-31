from flask_wtf.form import FlaskForm
from wtforms.fields.core import DateField, IntegerField, StringField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired, Optional

from models import Journal


class AddEntryForm(FlaskForm):
    journal_title = StringField(
        'Title',
        validators=[DataRequired()]
    )
    journal_date = DateField(
        'YYYY-MM-DD',
        validators=[DataRequired()],
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