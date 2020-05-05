# pylint: disable=method-hidden
from app.models import User
from flask_script import Command


class Seeder(Command):
    '''Seed the database with records'''

    def run(self):
        User(username='admin', password='password', is_admin=True).save()
        User(username='user', password='password', is_admin=False).save()
