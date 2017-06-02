from flask import Blueprint, request, render_template, json, Flask
from flask_sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt
from theroot.users_bundle.models.user import User
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from injector import Module, Key, provider, Injector, inject, singleton

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
db = SQLAlchemy(app)
'''
This class simply returns a user object.
It uses get_jwt_identity() which returns the username contained in the jwt token, 
in this case the username is the same e-mail address used for registration.
Therefore, being the e-mail address unique, we proceed querying the database to retrieve
the user object.
'''


class CurrentUserHelper:
    def __init__(self):
        pass

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

            if token_user_email:
                try:
                    user = User.query.filter_by(email=token_user_email).first()
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
