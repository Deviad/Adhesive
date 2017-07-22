from theroot.services import *
from theroot.users_bundle.models.user_info import address_user_table


class Address(db.Model):
    __tablename__ = 'addresses'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    address_line = db.Column(db.String(255), unique=False, nullable=False)
    zip = db.Column(db.String(255), unique=False, nullable=True)
    country = db.Column(db.String(255), unique=False, nullable=False)
    geohash = db.Column(db.String(255), unique=False, nullable=False)
    user_info = db.relationship("UserInfo", secondary=address_user_table, back_populates="addresses")

    def __init__(self, address, country, geohash, the_zip=None):
            self.address_line = address
            self.country = country
            self.geohash = geohash
            self.zip = the_zip

    def __repr__(self):
        return "<User (id='%r', address_line='%r', country='%r', geohash='%r', zip='%r', user_info='%r')>" \
               % (self.id, self.address_line, self.country, self.geohash, self.zip, self.user_info)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}