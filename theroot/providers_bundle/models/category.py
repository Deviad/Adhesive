from theroot.db import *
from theroot.providers_bundle.models.provider import category_provider_table
from sqlalchemy.orm.collections import attribute_mapped_collection

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    parent_id = db.Column(db.Integer, db.ForeignKey(id))
    name = db.Column(db.String(255), unique=True, nullable=False)
    providers = db.relationship("Provider", secondary=category_provider_table, back_populates="categories")
    children = db.relationship(
        "Category",
        # cascade deletions
        cascade="all, delete-orphan",

        # many to one + adjacency list - remote_side
        # is required to reference the 'remote'
        # column in the join condition.
        backref=db.backref("parent", remote_side=id),

        # children will be represented as a dictionary
        # on the "name" attribute.
        collection_class=attribute_mapped_collection('name'),
    )

    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent

    def __repr__(self):
        return "Category(name=%r, id=%r, parent_id=%r)" % (
            self.name,
            self.id,
            self.parent_id
        )

    def dump(self, _indent=0):
        return "   " * _indent + repr(self) + \
               "\n" + \
               "".join([
                   c.dump(_indent + 1)
                   for c in self.children.values()
               ])
