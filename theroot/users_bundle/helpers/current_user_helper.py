from pprint import pprint

from flask import Blueprint, request, render_template, json, Flask
from theroot.users_bundle.models.user import User
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import get_jwt_identity

from theroot.db import *

'''
This class simply returns a user object.
It uses get_jwt_identity() which returns the username contained in the jwt token, 
in this case the username is the same e-mail address used for registration.
Therefore, being the e-mail address unique, we proceed querying the database to retrieve
the user object.
'''


class CurrentUserHelper(User):
    def __init__(self):
        super().__init__(self.email, self.password)

# The difference between __init__ and __new__, is that __init__ returns only instances, objects of the same class,
# whereas __new__ can return something different. New is useful for cases like this where writing a factory would
# too much as we are returning one single function.

    def __new__(cls) -> User or bool:
        return cls.get_current_user()

    @classmethod
    def get_current_user(cls) -> User or bool:  # -> User or bool specifies that the output will be either
                                                # a user object or a boolean.
        if request.content_type == 'application/json':
            token_user_email = get_jwt_identity()
            print('the email in the token is ' + token_user_email)
            if token_user_email:
                try:
                    user = db.session.query(User).filter(User.email == token_user_email).first()
                    print('Our great user is here: ')
                    pprint(user)
                    return user
                except SQLAlchemyError as e:
                    db.session.close()
                    return e
                except AttributeError as e:
                    db.session.close()
                    return e
            else:
                response = json.jsonify({"status": "fail"})
                response.status_code = 401
                return response
