import json
import urllib
from pprint import pprint
from urllib import request, parse
import pytest

from inspect import getsourcefile
from os import path, sys
import sys

import sqlalchemy
from sqlalchemy.exc import SQLAlchemyError

current_dir = path.dirname(path.abspath(getsourcefile(lambda:0)))
sys.path.insert(0, current_dir[:current_dir.rfind(path.sep)])

from theroot.users_bundle.models.user import User
from theroot.users_bundle.controllers import do_the_signup
from theroot.services import *
from config import *
sys.path.pop(0)

from theroot import create_app


class TestApp(object):
    @pytest.fixture
    def app(self):
        myapp = create_app()
        myapp.config.from_object('config.TestingConfig')
        return myapp

    def test_create_user(self, client):
        values = {
            "data": {
                "email": "ziocaro02@gmail.com",
                "password": "test",
                "first_name": "ciccio",
                "last_name": "pizzo",
                "role": "1",
                "address": {
                    "country": "Italy",
                    "address_line": "Test Address, 1998, WXDJI Neverland, Italy",
                    "coordinates": {
                        "lat": "41.0914808",
                        "long": "16.8672337"
                    }
                }
            }

        }

        do_the_signup(values)
        rows = db.session.query(User.email).filter_by(email=values['data']['email']).all()
        results = [row for (row,) in rows]
        assert len(results) == 1

