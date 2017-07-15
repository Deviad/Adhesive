import json
import urllib
from pprint import pprint
from urllib import request, parse
import pytest

from inspect import getsourcefile
from os import path, sys
import sys
current_dir = path.dirname(path.abspath(getsourcefile(lambda:0)))
sys.path.insert(0, current_dir[:current_dir.rfind(path.sep)])

from theroot.users_bundle.models.user import User
from theroot.db import *
sys.path.pop(0)


class TestApp(object):
    def test_create_user(self):
        email = 'cicciorizzo02@gmail.com'
        password = 'thesuperpassword'
        user = User(email, password)
        db.session.add(user)
        db.session.commit()
        pprint(user.email)
        user_name = ', '.join(db.session.query(User.email).filter_by(email=user.email).first())
        assert user.email == user_name

