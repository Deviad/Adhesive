import json
import urllib
from pprint import pprint
from urllib import request, parse

import pytest
import sys


class TestApp(object):
    TEST_URL = 'http://0.0.0.0:5001'

    def test_create_user(self):

        values = {
            "data": {
                "email": "cicciopizzo88@gmail.com",
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

        headers = {
            "Content-Type": "application/json"
        }
        data = json.dumps(values).encode('utf8')
        url = TestApp.TEST_URL + '/api/user'
        req = urllib.request.Request(url, data=data, headers=headers)

        with urllib.request.urlopen(req) as response:
            the_page = response.read()
            the_page = json.loads(the_page)
            assert the_page['status'] == "success"
