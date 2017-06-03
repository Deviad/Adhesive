from functools import wraps

from flask import request, json
from theroot.users_bundle.helpers.current_user_helper import CurrentUserHelper


'''
This module provides a function decorator to use with your routing functions that allows to establish
who has access to a given resource. For the sake of clarity I associate some constants to the numbers that represent
each one of the access levels.
'''

ADMINISTRATOR_ONLY = 0
USER_ONLY = 1  # USER is the current user
ADMINISTRATOR_OR_USER = 2  # USER is the current user

# This is how we create function decorators in Python, which are used in order
# to modify the behavior of a function at run type.
# I use this pattern in order to separate the ACL logic from the "front-end" controller,
# making the code more solid.


def router_acl(user_type):
    def router_acl_decorator(fn):
        @wraps(fn)  # it basically updates the context with the new function, variables, etc.
        def func_wrapper(*args, **kwargs):
            current_user = CurrentUserHelper()

            if user_type == USER_ONLY:
                if current_user.id == int(request.args.get('user_id')):
                    return fn()
                else:
                    # you can test this by changing status to whatever you like and
                    # then trying to connect to a route with
                    # a wrong user id e.g. http://localhost:5001/api/user/edit?id=24
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
