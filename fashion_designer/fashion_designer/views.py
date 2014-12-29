import json
from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError
from pyramid.httpexceptions import (
    HTTPFound,
)

from .models import (
    DBSession,
    MyModel,
    SignUpSheet,
    Users,
    Profile,
)


# Check for duplicate email addresses
# Validate emails on the models side
@view_config(route_name='home', renderer='templates/mytemplate.jinja2')
def my_view(request):
    try:
        one = DBSession.query(MyModel).filter(MyModel.name == 'one').first()
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    return {'one': one, 'project': 'fashion_designer'}


@view_config(route_name='login', renderer='templates/login.jinja2')
def login(request):
    error = 'Invalid Username/Password'
    if 'form.submitted' in request.params:
        username = request.params['username']
        password = request.params['password']
        user = Users(username, password)
        if user.username_exists():
            return HTTPFound(request.route_url('home'))
        return {'error': error}
    return {'login': '/login'}


@view_config(route_name='signup', renderer='templates/signup.jinja2')
def signup(request):
    account_confirmed = "You've successfully signed up. \
                         An email has been sent out."
    error = 'An account with that email is already registered!'
    if 'form.submitted' in request.params:
        email = request.params['email']
        signee = SignUpSheet(email)
        if signee.is_duplicate_email():
            return {'error': error}
        DBSession.add(signee)
        request.session.flash(account_confirmed, 'is_confirmed')
        return HTTPFound(location=request.route_url('login'))
    return {'signup': '/signup'}


@view_config(route_name='users', request_method='GET',
             renderer='templates/index.jinja2')
def getUsers(request):
    #count = DBSession.query(SignUpSheet).order_by(SignUpSheet.id.asc()).all()
    count = DBSession.query(SignUpSheet).count()
    #return Response(
    #    body=json.dumps(
    return {'getUsers': count}
    #        status='200 OK',
    #        content_type='application/json'))


@view_config(route_name='profile', request_method='POST', renderer='json')
def createProfile(request):
    try:
        profile = Profile(age=request.params['age'],
                          sex=request.params['sex'],
                          location=request.params['location'],
                          style=request.params['style'])
        DBSession.add(profile)
    except:
        raise 'SQLALCHEMY ERROR'
    return Response(
        body=json.dumps({'createProfile': 'creating...'},
                        status='201 Created',
                        content_type='application/json'))


@view_config(route_name='profile', request_method='GET', renderer='json')
def getProfile(request):
    username = request.session('username')
    user_info = DBSession.query(Profile).filter_by(username=username).first()
    return Response(
        body=json.dumps({'getProfile': user_info},
                        status='200 OK',
                        content_type='application/json'))

conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_fashion_designer_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
