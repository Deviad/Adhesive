from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from theroot.users_bundle.controllers import users_bundle
from theroot.providers_bundle.controllers import categories_bundle
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.DevelopmentConfig')
    app.secret_key = app.config['JWT_SECRET_KEY']
    from theroot.db import db
    db.init_app(app)
    JWTManager(app)
    print('The token expires in ' + str(app.config['JWT_ACCESS_TOKEN_EXPIRES']))
    return app







