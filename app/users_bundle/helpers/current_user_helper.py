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

    def __new__(cls) -> User or bool:
        return cls.get_current_user()

    @classmethod
    def get_current_user(cls) -> User or bool:
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
