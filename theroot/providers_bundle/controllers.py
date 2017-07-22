from pprint import pprint
import sys
from flask import Blueprint, request, render_template, json, Flask
from theroot.providers_bundle.models import Category, Provider, category_provider_table

from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from theroot.users_bundle.helpers.router_acl import router_acl
from theroot.services import *

categories_bundle = Blueprint("categories_bundle", __name__, url_prefix="/api")


@categories_bundle.route("/category/add", methods=['POST'])
@jwt_required
@router_acl(3)
def add_category():
    try:

        if 'root_category' in request.json['data']:
            category = str(request.json['data']['root_category'])
            node = Category(category)
            # Category('node1', parent=node)
            db.session.add(node)
            db.session.commit()
        elif 'parent_category' in request.json['data'] and 'child_category' in request.json['data']:
            parent_category = request.json['data']['parent_category']
            child_category = request.json['data']['child_category']
            existing_category = Category.query.filter_by(name=request.json['data']['parent_category']).scalar()
            if parent_category != existing_category.name:
                response = json.jsonify({"status": "fail"})
                response.status_code = 400
                return response
            node = existing_category
            Category(child_category, node)
            db.session.add(node)
            db.session.commit()
        response = json.jsonify({"status": "success"})
        response.status_code = 201
        return response

    except BaseException:
        db.session.close()
        response = json.jsonify({"status": "fail"})
        response.status_code = 500
        return response

    except SQLAlchemyError:
        db.session.close()
        response = json.jsonify({"status": "fail"})
        response.status_code = 500
        return response
