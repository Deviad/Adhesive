from flask_sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity

db = SQLAlchemy()
jwt = JWTManager()
bcrypt = Bcrypt()
