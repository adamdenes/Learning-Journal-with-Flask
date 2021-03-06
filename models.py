import datetime

from peewee import *
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash

DATABASE = SqliteDatabase('journal.db')


class Journal(Model):
    title = CharField(max_length=255)
    date = DateTimeField(default=datetime.datetime.now)
    time_spent = IntegerField(default=0)
    learned = TextField()
    resources = TextField()

    class Meta:
        database = DATABASE
        order_by = ('-date',)  # order_by has been removed from Model Meta options in 3.6.0

    @classmethod
    def create_journal(cls, title, date, time_spent, learned, resources):
        try:
            with DATABASE.transaction():
                cls.create(
                    title=title,
                    date=date,
                    time_spent=time_spent,
                    learned=learned,
                    resources=resources
                )
        except IntegrityError:
            raise ValueError('Journal was not created!')


class User(UserMixin, Model):
    username = CharField(unique=True)
    password = CharField(unique=True)

    class Meta:
        database = DATABASE

    @classmethod
    def create_user(cls, username, password):
        try:
            with DATABASE.transaction():
                cls.get_or_create(
                    username=username,
                    password=generate_password_hash(password)
                )
        except IntegrityError:
            return User.get(User.username == username)


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Journal, User], safe=True)
    DATABASE.close()