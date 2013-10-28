""" Steward extension providing framework for web interface """
from pyramid.view import view_config


@view_config(route_name='root', renderer='index.jinja2')
def do_index(request):
    """ Render the index page """
    return {}


def _add_steward_web_app(config, title, name):
    """ Add a route to the list of steward web apps """
    config.registry.steward_web_apps.append((title, name))

def _web_apps(request):
    """ Get the list of steward web apps """
    return tuple(request.registry.steward_web_apps)

def includeme(config):
    """ Configure the app """

    config.add_route('root', '/')

    config.registry.steward_web_apps = []
    config.add_directive('add_steward_web_app', _add_steward_web_app)
    config.add_request_method(_web_apps, name='steward_web_apps', reify=True)

    config.scan()
