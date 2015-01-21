from pyramid.response import Response
from pyramid.view import view_config
from email import Emailer

from .models import (
    ApiKeys,
    DBSession,
    Users,
)

import json


@view_config(route_name='remote_login', renderer='json')
def login_validation(request):
    status = False
    session_key = request.matchdict['api_ses_key']
    username = request.params['username']
    password = request.params['password']
    key = ApiKeys.getSessionKey(session_key)
    if key:
        user = DBSession.query(Users).filter_by(username=username).first()
        if user.check_pswd_hash(password):
            status = True
        return Response(body=json.dumps(
            {"tag": "login", "status": status}),
            content_type="application/json")


@view_config(route_name='register', renderer='json')
def register(request):
    error_msg = None
    username = request.params['username']
    password = request.params['password']
    email = request.params['email']
    session_key = request.matchdict['api_ses_key']
    valid_key = ApiKeys.getSessionKey(session_key)
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
        return Response(body=json.dumps(
            {"tag": "register", "status": status, "error_msg": error_msg}),
            content_type="application/json")
