from functools import wraps
from pprint import pprint

import sys
from flask import request, json
from theroot.users_bundle.helpers.current_user_helper import CurrentUserHelper
from theroot.users_bundle.helpers.users_and_roles import get_user_roles

'''
This module provides a function decorator to use with your routing functions that allows to establish
who has access to a given resource. For the sake of clarity I associate some constants to the numbers that represent
each one of the access levels.
'''
# Constants representing the possible parameters passed into the decorator

ADMINISTRATOR_ONLY = 0
CURRENT_USER_ONLY = 1
ADMINISTRATOR_OR_CURRENT_USER = 2
ALL_REGISTERED_USERS = 3

# Constants representing the roles in the table

ADMINISTRATOR = 0
USER = 1

# This is how we create function decorators in Python, which are used in order
# to modify the behavior of a function at run type.
# I use this pattern in order to separate the ACL logic from the "front-end" controller,
# making the code more solid.


def router_acl(user_type):
    def router_acl_decorator(fn):
        @wraps(fn)  # it basically updates the context with the new function, variables, etc.
        def func_wrapper(*args, **kwargs):
            current_user = CurrentUserHelper()
            if request.method == 'GET':
                if user_type == CURRENT_USER_ONLY:
                    if current_user.id == int(request.args.get('user_id')):
                        return fn()
                    else:
                        # you can test this by changing status to whatever you like and
                        # then trying to connect to a route with
                        # a wrong user id e.g. http://localhost:5001/api/user/edit?id=24
                        response = json.jsonify({"status": "fail"})
                        response.status_code = 403
                        return response

                elif user_type == ADMINISTRATOR_ONLY:
                    roles = get_user_roles(current_user.id)
                    print('Let\'s print the user\'s roles')
                    pprint(roles)

                    if ADMINISTRATOR in roles:
                        return fn()
                    else:
                        response = json.jsonify({"status": "fail"})
                        response.status_code = 403
                        return response
                elif user_type == ADMINISTRATOR_OR_CURRENT_USER:
                    roles = get_user_roles(current_user.id)
                    if ADMINISTRATOR in roles or current_user.id == int(request.args.get('user_id')):
                        return fn()
                    else:
                        response = json.jsonify({"status": "fail"})
                        response.status_code = 403
                        return response
                elif user_type == ALL_REGISTERED_USERS:

                    roles = get_user_roles(current_user.id)
                    if USER in roles:
                        return fn()
                    else:
                        response = json.jsonify({"status": "fail"})
                        response.status_code = 403
                        return response
                        # this is a fallback in case no valid type is provided
                else:
                    response = json.jsonify({"status": "fail"})
                    response.status_code = 400
                    return response
            elif request.method == 'POST':
                if user_type == CURRENT_USER_ONLY:
                    print('let\'s print the request')
                    pprint(request.json)
                    print('let\'s print the current_user')
                    pprint(current_user)
                    if current_user.id == int(request.json['data']['id']):
                        return fn()

                    else:
                        response = json.jsonify({"status": "fail"})
                        response.status_code = 403
                        return response
                elif user_type == ADMINISTRATOR_ONLY:
                    roles = get_user_roles(current_user.id)
                    print('Let\'s print the user\'s roles')
                    pprint(roles)

                    if ADMINISTRATOR in roles:
                        return fn()
                    else:
                        response = json.jsonify({"status": "fail"})
                        response.status_code = 403
                        return response
                elif user_type == ADMINISTRATOR_OR_CURRENT_USER:
                    roles = get_user_roles(current_user.id)
                    if ADMINISTRATOR in roles or current_user.id == int(request.json['data']['id']):
                        return fn()
                    else:
                        response = json.jsonify({"status": "fail"})
                        response.status_code = 403
                        return response
                elif user_type == ALL_REGISTERED_USERS:
                    roles = get_user_roles(current_user.id)
                    if USER in roles:
                        return fn()
                    else:
                        response = json.jsonify({"status": "fail"})
                        response.status_code = 403
                        return response
                # this is a fallback in case no valid type is provided
                else:
                    response = json.jsonify({"status": "fail"})
                    response.status_code = 400
                    return response

        return func_wrapper
    return router_acl_decorator
