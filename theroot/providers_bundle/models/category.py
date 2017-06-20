# from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
# from sqlalchemy.orm import Session, relationship, backref, joinedload_all
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm.collections import attribute_mapped_collection


from theroot.db import *


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    parent_id = db.Column(db.Integer, db.ForeignKey(id))
    name = db.Column(db.String(255), nullable=False)

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
        collection_class=db.attribute_mapped_collection('name'),
    )

    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent

    def __repr__(self):
        return "TreeNode(name=%r, id=%r, parent_id=%r)" % (
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
