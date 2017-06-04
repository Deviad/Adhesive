
from theroot.db import *
from theroot.users_bundle.models import role_user_table


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.Integer, primary_key=True, autoincrement=False)
    users = db.relationship("User", secondary=role_user_table, back_populates="roles")

    def __init__(self, role_name):
        self.role = role_name

    def __repr__(self):
        return "<User (id='%r', role='%r')>" % (self.id, self.role)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
