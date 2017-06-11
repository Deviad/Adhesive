from theroot.db import *


address_user_table = db.Table('address_userinfo', db.Model.metadata,
                              db.Column('users_id', db.Integer, db.ForeignKey('users.id', onupdate="cascade"), nullable=False),
                              db.Column('addresses_id', db.Integer, db.ForeignKey('addresses.id', onupdate="cascade"), nullable=False))


class UserInfo(db.Model):
    __tablename__ = 'user_info'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(255), unique=False, nullable=False)
    last_name = db.Column(db.String(255), unique=False, nullable=False)
    facebook_id = db.Column(db.String(255), unique=True, nullable=True)
    linkedin_id = db.Column(db.String(255), unique=True, nullable=True)
    twitter_id = db.Column(db.String(255), unique=True, nullable=True)
    users_id = db.Column(db.Integer, db.ForeignKey('users.id', onupdate="cascade"), nullable=False)
    users = db.relationship("User", back_populates="user_info")  # user_info refers to the property in User class.
    addresses = db.relationship("Address", secondary=address_user_table, back_populates="user_info")

# def __init__(self, **kwargs):
    #     for key, value in kwargs.items():
    #         setattr(self, key, value)

    def __init__(self, first_name, last_name, users_id, facebook_id=None, linkedin_id=None, twitter_id=None):
        self.first_name = first_name
        self.last_name = last_name
        self.facebook_id = facebook_id
        self.linkedin_id = linkedin_id
        self.twitter_id = twitter_id
        self.users_id = users_id

    def __repr__(self):
        return "<User (id='%r', user_id='%r', first_name='%r', last_name='%r', \
        facebook_id='%r', linkedin_id='%r', twitter_id='%r')>" \
        % (self.id, self.users_id, self.first_name, self.last_name, self.facebook_id, self.linkedin_id, self.twitter_id)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
