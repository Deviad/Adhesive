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


def current_user_only(fn):
    def ret_fn(*args, **kwargs):
        current_user = CurrentUserHelper()

        if current_user.id == int(request.args.get('id')):
            return fn()
        else:
            # you can test this by changing status to whatever you like and then trying to connect to a route with
            # a wrong user id e.g. http://localhost:5001/api/user/edit?id=24
            response = json.jsonify({"status": "fail"})
            response.status_code = 403
            return response
    return ret_fn
