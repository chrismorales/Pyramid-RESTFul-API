import os
import shutil
from pyramid.response import Response
from pyramid.view import (
    view_config,
    forbidden_view_config,
)
from pyramid.security import (
    remember,
    forget,
)
from email import Emailer

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
    SystemMessages,
)


# Check for duplicate email addresses
# Validate emails on the models side
@view_config(route_name='home', renderer='templates/mytemplate.jinja2',
             permission='view')
def my_view(request):
    registration_confirmed = "Your account has been successfully registered!"
    if 'register_form.submitted' in request.params:
        username = request.params['username']
        password = request.params['password']
        email = request.params['email']
        account = Users(username, password, email)
        if account.username_exists():
            return {'error': 'Username exists'}
        DBSession.add(account)
        request.session.flash(registration_confirmed, 'confirmed')
        return HTTPFound(location=request.route_url('login'))
    try:
        one = DBSession.query(MyModel).filter(MyModel.name == 'one').first()
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    return dict(
        one=one,
        project='fashion_designer',
        register=True,
        logged_in=request.authenticated_userid
    )


@view_config(route_name='login', request_method='GET',
             renderer='templates/login.jinja2')
def getlogin(request):
    login = request.route_url('login')
    return dict(
        login=login
    )


@forbidden_view_config(renderer='templates/login.jinja2')
@view_config(route_name='login', request_method='POST',
             renderer='templates/login.jinja2')
def login(request):
    error = 'Invalid Username/Password'
    if 'form.submitted' in request.params:
        username = request.params['username']
        password = request.params['password']
        user = DBSession.query(Users).filter_by(username=username).first()
        if user:
            if user.check_pswd_hash(password):
                headers = remember(request, username)
                return HTTPFound(
                    location=request.route_url('home'),
                    headers=headers
                )
        return dict(
            error=error
        )


@view_config(route_name='logout')
def logout(request):
    headers = forget(request)
    return HTTPFound(
        location=request.route_url('home'),
        headers=headers
    )


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
        mailer = Emailer(email, request)
        mailer.send_message()
        request.session.flash(account_confirmed, 'is_confirmed')
        return HTTPFound(location=request.route_url('login'))
    return dict(
        signup='/signup',
        logged_in=request.authenticated_userid
    )


@view_config(route_name='users', request_method='GET',
             renderer='templates/index.jinja2', permission='view')
def getUsers(request):
    users = DBSession.query(SignUpSheet).order_by(SignUpSheet.id.asc()).all()
    count = DBSession.query(SignUpSheet).count()
    # return Response(
    #    body=json.dumps(
    return dict(
        getUsers=count,
        user_list=users,
        logged_in=request.authenticated_userid
    )
    #        status='200 OK',
    #        content_type='application/json'))


@view_config(route_name='add_messages', request_method='GET',
             renderer='templates/system_messages.jinja2')
def get_sys_messages(request):
    messages = DBSession.query(SystemMessages).order_by("id asc").all()
    return dict(
        messages=messages,
        logged_in=request.authenticated_userid
    )


@view_config(route_name='add_messages', request_method='POST',
             renderer='templates/system_messages.jinja2')
def add_sys_messages(request):
    confirmation = 'Message has been added!'
    if 'msg.submitted' in request.params:
        page = request.params['page']
        msg = request.params['msg']
        message = SystemMessages(page, msg)
        DBSession.add(message)
        request.session.flash(confirmation)
        return HTTPFound(location=request.route_url('add_messages'))
    return dict(
        getMessages=None,
        logged_in=request.authenticated_userid
    )


@view_config(route_name='profile', request_method='GET',
             renderer='templates/profile/profile.jinja2')
def getProfile(request):
    id = request.matchdict['id']
    user_info = DBSession.query(Users).filter_by(user_id=id).first()
    return dict(
        user=user_info,
        logged_in=request.authenticated_userid
    )


@view_config(route_name='profile', request_method='POST',
             renderer='templates/profile/profile.jinja2')
def createProfile(request):
    age = request.params['age']
    sex = request.params['sex']
    location = request.params['location']
    style = request.params['style']
    user_id = request.matchdict['id']
    if "form.submitted" in request.params:
        profile = Profile(
            user_id,
            age,
            sex,
            location,
            style
        )
        DBSession.add(profile)
        return HTTPFound(location=request.route_url('profile', id=user_id))


@view_config(route_name='store_mp3_view')
def store_mp3_view(request):
    if "photo.submitted" in request.params:

        filename = request.POST['mp3'].filename
        input_file = request.POST['mp3'].file

        file_path = os.path.join('/tmp', filename)
        with open(file_path, 'wb') as output_file:
            shutil.copyfileobj(input_file, output_file)
        return HTTPFound(request.route_url('home'))


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
