from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    MyModel,
    SignUpSheet,
    )


@view_config(route_name='home', renderer='templates/mytemplate.jinja2')
def my_view(request):
    print request.params
    if 'form.submitted' in request.params:
        email = request.params['email']
        add_email = SignUpSheet(email);
        DBSession.add(add_email)
    try:
        one = DBSession.query(MyModel).filter(MyModel.name == 'one').first()
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    return {'one': one, 'project': 'fashion_designer'}

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

