""" Steward extension providing framework for web interface """
import re

import pyramid.renderers
from pyramid.request import Request
from pyramid.settings import asbool


def to_json(value):
    """ A json filter for jinja2 """
    return pyramid.renderers.render('json', value)


def do_index(request):
    """ Render the index page """
    return {}


def _add_steward_web_app(config, title, name):
    """ Add a route to the list of steward web apps """
    config.registry.steward_web_apps.append((title, name))


def _web_apps(request):
    """ Get the list of steward web apps """
    return tuple(request.registry.steward_web_apps)


def _route_names(request, pattern=r'.*'):
    """ Get a list of route names that match the pattern """
    pattern = re.compile('^' + pattern + '$')
    introspector = request.registry.introspector
    routes = introspector.get_category('routes')
    names = []
    for route in routes:
        name = route['introspectable']['name']
        if pattern.match(name):
            names.append(name)
    return names


def _route_map(request, pattern=r'.*'):
    """ Get a dict of route names to route urls """
    return {name: request.route_url(name) for name in
            request.route_names(pattern)}


def includeme(config):
    """ Configure the app """
    settings = config.get_settings()

    config.add_route('root', '/')
    config.add_view('steward_web.do_index', route_name='root',
                    renderer='index.jinja2')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')

    config.registry.steward_web_apps = []
    config.add_directive('add_steward_web_app', _add_steward_web_app)
    config.add_request_method(_web_apps, name='steward_web_apps', reify=True)
    config.add_request_method(_route_names, name='route_names')
    config.add_request_method(_route_map, name='route_map')

    if asbool(settings.get('steward.web.basic_login', True)):
        config.scan()
