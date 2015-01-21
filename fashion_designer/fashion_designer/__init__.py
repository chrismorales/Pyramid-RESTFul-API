from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from fashion_designer.security import groupfinder

from pyramid.config import Configurator
from pyramid_mailer.mailer import Mailer
from pyramid.session import SignedCookieSessionFactory
from sqlalchemy import engine_from_config

from .models import (
    DBSession,
    Base,
    )

mailer = Mailer()


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    my_session_factory = SignedCookieSessionFactory('itsaseekreet')
    authn_policy = AuthTktAuthenticationPolicy(
        'sosecret', callback=groupfinder, hashalg='sha512')
    authz_policy = ACLAuthorizationPolicy()
    config = Configurator(settings=settings,
                          session_factory=my_session_factory,
                          root_factory='fashion_designer.models.RootFactory')
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)
    config.include('pyramid_jinja2')
    config.include('pyramid_mailer')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.include(add_routes)
    config.include(api_routes)
    return config.make_wsgi_app()


def add_routes(config):
    config.add_route('home', '/')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('signup', '/signup')
    config.add_route('profile', '/profile/{id}')
    config.add_route('users', '/users')
    config.add_route('add_messages', '/add_system_messages')
    config.add_route('ajax', '/ajax')
    config.scan()


def api_routes(config):
    config.add_routes('remote_login', '/login/{api_key}')
    config.add_routes('register', '/register/{api_key}')
    config.add_routes('user_profile', '/profile/{user_id}')
