from pprint import pprint

import sys

from theroot.db import db
from theroot.users_bundle.models import User
from theroot.users_bundle.models import Role

# 0 is the admin role
# 1 is the user role

# this query retrieves all the roles associated to a user


def get_user_roles(user_id):

    the_roles = db.session.query(Role.role).filter(Role.users.any(id=user_id)).all()
    pprint(the_roles)
    response = []
    length = len(the_roles)
    for key in range(length):
        the_roles[key] = list(the_roles[key])
        response.append(the_roles[key][0])

    return response
    # return db.session.query(Role.role).filter(User.id == user_id).all()


def get_users_by_role():
    pass
