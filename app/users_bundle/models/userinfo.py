from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
db = SQLAlchemy(app)


class UserInfo(db.Model):
    __tablename__ = 'user_info'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('id'))
    first_name = db.Column(db.String(255), unique=False, nullable=False)
    last_name = db.Column(db.String(255), unique=False, nullable=False)
    facebook_id = db.Column(db.String(255), unique=True, nullable=True)
    linkedin_id = db.Column(db.String(255), unique=True, nullable=True)
    twitter_id = db.Column(db.String(255), unique=True, nullable=True)

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def __repr__(self):
        return "<User (id='%r', user_id='%r', first_name='%r', last_name='%r', \
        facebook_id='%r', linkedin_id='%r', twitter_id='%r')>" \
        % (self.id, self.user_id, self.first_name, self.last_name, self.facebook_id, self.linkedin_id, self.twitter_id)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
