from pyramid.config import Configurator
from pyramid.session import SignedCookieSessionFactory
from sqlalchemy import engine_from_config

from .models import (
    DBSession,
    Base,
    )


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    my_session_factory = SignedCookieSessionFactory('itsaseekreet')
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    # settings = {
    #    'mail.host': 'localhost',
    #    'mail.port': '25',
    #    'username': 'nogareru@gmail.com',
    #    'password': 'who escaped.qpwoei3#'
    # }
    config = Configurator(settings=settings)
    config.set_session_factory(my_session_factory)
    config.include('pyramid_jinja2')
    config.include('pyramid_mailer')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.include(add_routes)
    return config.make_wsgi_app()


def add_routes(config):
    config.add_route('home', '/')
    config.add_route('add_messages', '/add_system_messages')
    config.add_route('login', '/login')
    config.add_route('signup', '/signup')
    config.add_route('profile', '/profile/{id}')
    config.add_route('users', '/users')
    config.scan()
