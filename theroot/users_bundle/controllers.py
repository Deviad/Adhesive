import cgi
from pprint import pprint
import sys

from flask import Blueprint, request, render_template, json, Flask


from theroot.users_bundle.models.user import User, role_user_table
from theroot.users_bundle.models import UserInfo, Role, Address

from sqlalchemy.exc import SQLAlchemyError
from theroot.users_bundle.helpers.router_acl import router_acl
from theroot.services import *
from html import escape, unescape
import urllib.request
from geohash import encode as geoe, decode as geod



users_bundle = Blueprint("users_bundle", __name__, url_prefix="/api")




def hash_password(password):
    pw_hash = bcrypt.generate_password_hash(password)
    return pw_hash

def do_the_signin(the_email, password):
    try:
        user = User.query.filter_by(email=the_email).first()
        db.session.close()
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

@users_bundle.route("/user/validate_address", methods=['POST'])
def validate_address(*args, **kwargs):
    if request.method == 'POST':
        if request.content_type == 'application/json':

            if 'address' in request.json['data']:
                address = request.json['data']['address']
                converted_address = str(cgi.escape(address.replace(" ", "%20").replace(',',  "%44;")).encode("ascii", "xmlcharrefreplace"),'utf-8')
                print(converted_address)
                pprint('https://maps.googleapis.com/maps/api/place/autocomplete/json?input=' + converted_address + '&types=address' + '&key=' + app.config.get('GOOGLE_PLACES_API_KEY'))
            if 'place_id' in request.json['data']:
                place_id = request.json['data']['place_id']
            # pprint(address)

        try:
            if not request.json['data']['selected']:
                with urllib.request.urlopen('https://maps.googleapis.com/maps/api/place/autocomplete/json?input=' + converted_address + '&types=address' + '&key=' + app.config.get('GOOGLE_PLACES_API_KEY')) as response:
                    google_json = json.loads(response.read())
                response.status_code = 200
                status = 'success'
                if google_json['status'] != 'OK':
                    response.status_code = 400
                    status = 'fail'
                response = json.jsonify({"status": status, "data": google_json})
                return response
            else:
                with urllib.request.urlopen('https://maps.googleapis.com/maps/api/place/details/json?placeid=' + place_id + '&key=' + app.config.get('GOOGLE_PLACES_API_KEY')) as response:
                    google_json = json.loads(response.read())
            response.status_code = 200
            status = 'success'
            if google_json['status'] != 'OK':
                response.status_code = 400
                status = 'fail'
            response = json.jsonify({"status": status, "data": google_json})
            return response
        except BaseException:
            response = json.jsonify({"status": "fail"})
            response.status_code = 500
            return response


def do_the_signup(json_attributes):
  
    # try:
        user = User(json_attributes['data']['email'], hash_password(json_attributes['data']['password']))
        db.session.add(user)
        db.session.commit()
        user = User.query.filter_by(email=json_attributes['data']['email']).first()

        address_line = json_attributes['data']['address']['address_line']

        country = json_attributes['data']['address']['country']
        coordinates = json_attributes['data']['address']['coordinates']
        geohash = geoe(float(coordinates['lat']), float(coordinates['long']))

        address = Address(address_line, country, geohash)
        db.session.add(address)

        user_info = UserInfo(json_attributes['data']['first_name'], json_attributes['data']['last_name'], user.id)
        db.session.add(user_info)
        db.session.commit()
        if 'role' in json_attributes['data']:
            if int(json_attributes['data']['role']) in range(1, 2):
                role = Role.query.filter_by(id=json_attributes['data']['role']).first()
                user.roles.append(role)
                db.session.commit()
        db.session.close()
        # using jsend standard https://labs.omniti.com/labs/jsend
        response = json.jsonify({"status": "success"})
        response.status_code = 201
        return response

    # except SQLAlchemyError:
    #     db.session.close()
    #     response = json.jsonify({"status": "fail"})
    #     response.status_code = 400
    #     return response
    # except BaseException:
    #     db.session.close()
    #     response = json.jsonify({"status": "fail"})
    #     response.status_code = 500
    #     return response


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
@router_acl(3)
def view_user():
    if request.method == 'GET':
        if request.content_type == 'application/json':
            request_user_id = int(request.args.get('user_id'))
            if User.query.filter_by(id=request_user_id).scalar():
                request_user = User.query.filter_by(id=request_user_id).first()
                request_user_info = UserInfo.query.filter_by(users_id=request_user_id).first()
                response = json.jsonify({"status": "success",
                                         "data": {'user': request_user.as_dict(),
                                                  'user_info': request_user_info.as_dict()
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
@router_acl(2)
def edit_user():
    only = ['email', 'password', 'first_name', 'last_name', 'facebook_id', 'linkedin_id', 'twitter_id']
    email_change = False
    if request.method == 'POST':
        if request.content_type == 'application/json':
            request_user_id = int(request.json['data']['id'])
            if request_user_id:
                request_user = User.query.filter_by(id=request_user_id).first()
                request_user_info = UserInfo.query.filter_by(users_id=request_user_id).first()
                for key, value in request.json['data'].items():
                    if key in only:
                        if key == 'email':
                            # we use join to extract the items in the list.
                            # db.session.query returns a tuple that needs to be converted into a string in this case.
                            database_email = ', '.join(db.session.query(User.email).filter_by(id=request_user.id).first())
                            setattr(request_user, key, value)
                            # print('Has current user email ' + str(current_user.email))
                            # print('Has database email ' + str(database_email))
                            if request_user.email != database_email:
                                email_change = True
                                # print('Has email chaned? ' + str(email_change))
                        if key == 'password':
                            setattr(request_user, key, bcrypt.generate_password_hash(value))
                        else:
                            setattr(request_user_info, key, value)
                pprint(request_user)
                db.session.commit()
                # print('Has email changed? ' + str(email_change))

                # db.session.add(current_user)
                if email_change:
                    print('Printing again the email ' + request_user.email)
                    response = json.jsonify(
                        {"status": "success",
                         "data": {
                             "access_token": create_access_token(identity=request_user.email)

                         }
                         })
                else:
                    response = json.jsonify({"status": "success"})
                db.session.close()
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
            username = request.json['data']['email']
            password = request.json['data']['password']
            # password = request.args.get('password')
            return do_the_signin(username, password)
