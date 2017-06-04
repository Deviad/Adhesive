from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from theroot.users_bundle.models import *

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')

db = SQLAlchemy(app)


manager = Manager(app)


class DB(object):
    def __init__(self, metadata):
        self.metadata = metadata


@manager.command
def seed():
    print('Add seed data to the database.')
    for i in range(2):
        the_role = Role(i)
        db.session.add(the_role)
    db.session.commit()
    db.session.close()

migrate = Migrate(app, DB(db.Model.metadata))

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()



