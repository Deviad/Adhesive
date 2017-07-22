from flask_sqlalchemy import SQLAlchemy
from .user import User
from .user import role_user_table
from .user_info import UserInfo
from .role import Role
from .address import Address
from .user_info import address_user_table
db = SQLAlchemy()
