
from theroot.users_bundle.models import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), unique=False, nullable=False)
    user_info = db.relationship("UserInfo", uselist=False, back_populates="users")

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def __repr__(self):
        return "<User (id='%r', email='%r', password='%r')>" % (self.id, self.email, self.password)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
