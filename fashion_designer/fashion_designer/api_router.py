from pyramid.response import Reponse
from pyramid.view import view_config
from email import Emailer

from .models import (
    ApiKeys,
)

import json


@view_config(route_name='remote_login', renderer='json')
def login_validation(request):
    get_remote_session_key = request.params['api_ses_key']
    key = ApiKeys.getSessionKey(get_remote_session_key)
    if key:
        msg = "Key exists!"
    else:
        msg = "Key doesn't exists!"
    return Reponse(body=json.dumps(
        {"msg": msg}),
        content_type="application/json")
