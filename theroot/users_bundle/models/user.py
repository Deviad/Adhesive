from theroot.services import *

role_user_table = db.Table('role_user', db.Model.metadata,
                           db.Column('users_id', db.Integer, db.ForeignKey('users.id', onupdate="cascade"), nullable=False),
                           db.Column('roles_id', db.Integer, db.ForeignKey('roles.id', onupdate="cascade"), nullable=False))


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), unique=False, nullable=False)
    user_info = db.relationship("UserInfo", uselist=False, back_populates="users")
    roles = db.relationship("Role", secondary=role_user_table, back_populates="users")

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def __repr__(self):
        return "<User (id='%r', email='%r', password='%r')>" % (self.id, self.email, self.password)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
