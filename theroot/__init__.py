from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from theroot.users_bundle.controllers import users_bundle
from theroot.providers_bundle.controllers import categories_bundle


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.DevelopmentConfig')
    app.secret_key = app.config['JWT_SECRET_KEY']
    from theroot.services import db
    from theroot.services import jwt
    from theroot.services import bcrypt
    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    print('The token expires in ' + str(app.config['JWT_ACCESS_TOKEN_EXPIRES']))
    return app







