from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from theroot.users_bundle.controllers import users_bundle
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from theroot.db import *


app.secret_key = app.config['JWT_SECRET_KEY']
jwt = JWTManager(app)
print('The token expires in ' + str(app.config['JWT_ACCESS_TOKEN_EXPIRES']))
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
if not database_exists(engine.url):
    print('Creating the database')
    create_database(engine.url)
else:
    print('The database exists: ' + str(database_exists(engine.url)))
app.register_blueprint(users_bundle)

Bcrypt(app)

