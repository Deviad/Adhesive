from flask import Blueprint, request, render_template, json, Flask
from flask_sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt
from app.users_bundle.models.user import User
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from injector import Module, Key, provider, Injector, inject, singleton

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
db = SQLAlchemy(app)


class CurrentUserHelper:
    def __init__(self):
        pass

    def __new__(cls):
        return cls.get_current_user()

    @classmethod
    def get_current_user(cls) -> User or bool:
        if request.content_type == 'application/json':
            user_id = request.args.get('id')
            token_user_email = get_jwt_identity()
            parameter_user_email = None
            try:
                for email in db.session.query(User.email).filter_by(id=user_id).one():
                    parameter_user_email = email
            except SQLAlchemyError as e:
                db.session.close()
                return e
            except AttributeError as e:
                db.session.close()
                return e
            if token_user_email == parameter_user_email:
                user = User.query.filter_by(id=user_id).first()
                return user
            else:
                db.session.close()
                return False
