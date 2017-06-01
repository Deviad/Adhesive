from flask import Blueprint, request, render_template, json, Flask
from flask_sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt

from app.users_bundle.helpers.current_user_helper import CurrentUserHelper
from app.users_bundle.models.user import User
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from injector import Module, Key, provider, Injector, inject, singleton

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
db = SQLAlchemy(app)

ADMINISTRATOR_ONLY = 0
USER_ONLY = 1  # user is the current user
ADMINISTRATOR_OR_USER = 2  # user is the current user


def router_acl(user_type):
    def router_acl_decorator(fn):
        def func_wrapper(*args, **kwargs):
            current_user = CurrentUserHelper()

            if user_type == USER_ONLY:
                if current_user.id == int(request.args.get('id')):
                    return fn()
                else:
                    # you can test this by changing status to whatever you like and
                    # then trying to connect to a route with
                    # a wrong user id e.g. http://localhost:5001/api/user/edit?id=24
                    response = json.jsonify({"status": "fail"})
                    response.status_code = 403
                    return response
            # this is a fallback in case no valid type is provided
            else:
                response = json.jsonify({"status": "fail"})
                response.status_code = 500
                return response
        return func_wrapper
    return router_acl_decorator
