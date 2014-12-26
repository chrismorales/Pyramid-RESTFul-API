from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError
from pyramid.httpexceptions import (
    HTTPFound,
    HTTPNotFound,
)

from .models import (
    DBSession,
    MyModel,
    SignUpSheet,
    Users,
)


# Check for duplicate email addresses
# Validate emails on the models side
@view_config(route_name='home', renderer='templates/mytemplate.jinja2')
def my_view(request):
    account_confirmed = "You've successfully signed up. An email has been sent out."
    if 'form.submitted' in request.params:
        email = request.params['email']
        add_email = SignUpSheet(email);
        check_email = add_email.is_duplicate_email()
        if check_email:
            return { 'error': 'Email exists already.'}
        DBSession.add(add_email)
        return { 'msg': account_confirmed, 'is_confirmed': True}
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
    error = 'An account with that email is already registered!'
    if 'form.submitted' in request.params:
        email = request.params['email']
        signee = SignUpSheet(email)
        if signee.is_duplicate_email():
            return {'error': error}
        else:
            DBSession.add(signee)
            return HTTPFound(request.route_url('login'))
    return {'signup': '/signup'}


@view_config(request_method='GET', renderer='json')
def getUsers(self):
    count = DBSession.query(SignUpSheet).count()
    return Response(count,
                    content_type='text/json',
                    status_int=200)


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

