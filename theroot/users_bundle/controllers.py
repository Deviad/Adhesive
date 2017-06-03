from inspect import getmembers
from pprint import pprint

import sys
from flask import Blueprint, request, render_template, json, Flask
from flask_sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt

from theroot.users_bundle.models.user import User
from theroot.users_bundle.models import UserInfo

from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from theroot.users_bundle.helpers.current_user_helper import CurrentUserHelper
from theroot.users_bundle.helpers.router_acl import router_acl

bcrypt = Bcrypt()
db = SQLAlchemy()


users_bundle = Blueprint("user", __name__, url_prefix="/api")


def hash_password(password):
    pw_hash = bcrypt.generate_password_hash(password)
    return pw_hash


def do_the_signin(the_email, password):
    try:
        user = User.query.filter_by(email=the_email).first()
        pw_hash = user.password
        if bcrypt.check_password_hash(pw_hash, password):
            response = json.jsonify({"status": "success", "data": {"access_token": create_access_token(identity=user.email)}})
            response.status_code = 200
            return response
        else:
            response = json.jsonify({"status": "fail"})
            response.status_code = 401
            return response

    except (SQLAlchemyError, AttributeError):
        db.session.close()
        response = json.jsonify({"status": "fail"})
        response.status_code = 500
        return response


def do_the_signup(json_attributes):
  
    try:
        user = User(json_attributes['email'], hash_password(json_attributes['password']))

        db.session.add(user)
        db.session.commit()
        user = User.query.filter_by(email=json_attributes['email']).scalar()
        user_info = UserInfo(json_attributes['first_name'], json_attributes['last_name'], user.id)
        db.session.add(user_info)
        db.session.commit()
        db.session.close()
        # using jsend standard https://labs.omniti.com/labs/jsend
        response = json.jsonify({"status": "success"})
        response.status_code = 201
        return response

    except SQLAlchemyError:
        db.session.close()
        response = json.jsonify({"status": "fail"})
        response.status_code = 400
        return response


@users_bundle.route("/user", methods=['POST'])
def signup():
    if request.method == 'POST':
        if request.content_type == 'application/json':
            # pprint(request.json)
            # sys.exit()
            # password = request.args.get('password')
            return do_the_signup(request.json)


@users_bundle.route("/user/view", methods=['GET'])
@jwt_required
@router_acl(1)
def view_user():
    if request.method == 'GET':
        if request.content_type == 'application/json':
            current_user = CurrentUserHelper()
            pprint(current_user.id)
            current_user_info = UserInfo.query.filter_by(users_id=current_user.id).first()
            if current_user:
                response = json.jsonify({"status": "success",
                                         "data": {'user': current_user.as_dict(),
                                                  'user_info': current_user_info.as_dict()
                                                  }
                                         })
                response.status_code = 200
                return response
            else:
                db.session.close()
                response = json.jsonify({"status": "fail"})
                response.status_code = 403
                return response


@users_bundle.route("/user/edit", methods=['POST'])
@jwt_required
@router_acl(1)
def edit_user():
    if request.method == 'POST':
        if request.content_type == 'application/json':
            current_user = CurrentUserHelper()
            pprint(current_user.id)
            current_user_info = UserInfo.query.filter_by(users_id=current_user.id).first()
            if current_user:
                response = json.jsonify({"status": "success",
                                         "data": {'user': current_user.as_dict(),
                                                  'user_info': current_user_info.as_dict()
                                                  }
                                         })
                response.status_code = 200
                return response
            else:
                db.session.close()
                response = json.jsonify({"status": "fail"})
                response.status_code = 403
                return response


@users_bundle.route("/auth", methods=['POST'])
def signin():
    if request.method == 'POST':
        if request.content_type == 'application/json':
            username = request.json['email']
            password = request.json['password']
            # password = request.args.get('password')
            return do_the_signin(username, password)
