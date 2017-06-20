
from theroot.db import *


class Provider(db.Model):
    __tablename__ = 'providers'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Integer, unique=True, autoincrement=False)
    category = db.Column(db.String(255), unique=False, nullable=False)


    def __init__(self, the_name):
        self.name = the_name

    def __repr__(self):
        return "<User (id='%r', name='%r', category='%r')>" % (self.id, self.name, self.category)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
