import datetime

from peewee import *


DATABASE = SqliteDatabase('journal.db')


class Journal(Model):
    id = AutoField()
    title = CharField(max_length=255, unique=True)
    date = DateTimeField(default=datetime.datetime.now)
    time_spent = IntegerField(default=0)
    learned = TextField()
    resources = TextField()

    class Meta:
        database = DATABASE
        order_by = ('-date',)

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
            raise ValueError('Journal with that title already exist!')


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Journal], safe=True)
    DATABASE.close()
