
from theroot.services import *

category_provider_table = db.Table('category_provider', db.Model.metadata,
                           db.Column('providers_id', db.Integer, db.ForeignKey('providers.id', onupdate="cascade"), nullable=False),
                           db.Column('categories_id', db.Integer, db.ForeignKey('categories.id', onupdate="cascade"), nullable=False))


class Provider(db.Model):
    __tablename__ = 'providers'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Integer, unique=True, autoincrement=False)
    categories = db.relationship("Category", secondary=category_provider_table, back_populates="providers")

    def __init__(self, the_name):
        self.name = the_name

    def __repr__(self):
        return "<User (id='%r', name='%r', category='%r')>" % (self.id, self.name, self.category)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
