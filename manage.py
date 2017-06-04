from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

role_user_table = db.Table('role_user', db.Model.metadata,
                           db.Column('users_id', db.Integer, db.ForeignKey('users.id')),
                           db.Column('roles_id', db.Integer, db.ForeignKey('roles.id')))


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), unique=False, nullable=False)
    user_info = db.relationship("UserInfo", uselist=False, back_populates="users")
    roles = db.relationship("Role", secondary=role_user_table, back_populates="users")


class UserInfo(db.Model):
    __tablename__ = 'user_info'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), unique=False, nullable=False)
    last_name = db.Column(db.String(255), unique=False, nullable=False)
    facebook_id = db.Column(db.String(255), unique=True, nullable=True)
    linkedin_id = db.Column(db.String(255), unique=True, nullable=True)
    twitter_id = db.Column(db.String(255), unique=True, nullable=True)
    users_id = db.Column(db.Integer, db.ForeignKey('users.id', onupdate="cascade"), nullable=False)
    users = db.relationship("User", back_populates="user_info")  # user_info refers to the property in User class.


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.Integer, unique=True, nullable=False)
    users = db.relationship("User", secondary=role_user_table, back_populates="roles")


@manager.command
def seed():
    print('Add seed data to the database.')
    role = Role(1)
    db.session.add(role)
    db.session.commit()
    db.session.close()


if __name__ == '__main__':
    manager.run()



