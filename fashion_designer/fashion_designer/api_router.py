from pyramid.response import Response
from pyramid.request import Request
from pyramid.view import view_config
from email import Emailer

from .models import (
    ApiKeys,
    DBSession,
    Users,
)

import json


@view_config(route_name='remote_login', request_method="POST", renderer='json')
def login_validation(request):
    error_msg = None
    session_key = request.matchdict['api_key']
    username = request.params['username']
    password = request.params['password']

    api_key = ApiKeys()
    valid_key = api_key.getSessionKey(session_key)
    if valid_key:
        user = DBSession.query(Users).filter_by(username=username).first()
        if user.check_pswd_hash(password):
            status = True
        else:
            error_msg = "Invalid Username/Password!"
            status = False
    else:
        error_msg = "API Key Invalid"
    return Response(body=json.dumps(
        {
            "tag": "login",
            "status_code": "200 OK",
            "status": status,
            "error_msg": error_msg
        }
    ),
        content_type="application/json")


@view_config(route_name='register', request_method="POST", renderer='json')
def register(request):
    error_msg = None

    username = request.params['username']
    password = request.params['password']
    email = request.params['email']

    session_key = request.matchdict['api_key']
    api_key = ApiKeys()
    valid_key = api_key.getSessionKey(session_key)

    if valid_key:
        # Register the user
        user = Users(username, password, email)
        if user.username_exists():
            status = False
            error_msg = "Username already exists!"
        else:
            status = True
            DBSession.add(user)
            mailer = Emailer(email, request)
            mailer.send_message()
    else:
        status = False
        error_msg = "API Key Invalid!"

    # Send the Response back to the android device
    return Response(body=json.dumps(
        {"tag": "register", "status": status, "error_msg": error_msg}),
        content_type="application/json")

"""
@view_config(route_name='create_profile', request_method="POST",
             renderer='json')
def create_profile(request):
    pass


@view_config(route_name="get_profile", request_method="GET", renderer="json")
def get_profile(request):
    pass
"""


@view_config(route_name='api', request_method="GET")
def validateAPISession(request):
    """
        This will check that the session key is always valid before calling
        any routes.
    """
    # Check if the session key exists?
    api_key = request.matchdict['api_key']
    valid_key = DBSession.query(ApiKeys).filter_by(session_key=api_key).first()
    if valid_key.getSession():
        route_path = request.params['route']
        # call a subrequest to the proper functions
        subreq = Request.blank(route_path)
        response = request.invoke_subrequest(subreq)
        return response
