""" Views for basic username/password auth """
import logging
from pyramid.httpexceptions import HTTPFound, HTTPForbidden
from pyramid.security import NO_PERMISSION_REQUIRED, forget, remember
from pyramid.view import view_config


LOG = logging.getLogger(__name__)


def _get_app_root(request):
    """ Get the root url of the app """
    try:
        return request.route_url('root')
    except KeyError:
        LOG.warn("Steward has no 'root' route_name. Using '/' instead")
        return '/'


@view_config(route_name='logout')
def do_logout(request):
    """ Delete the user's auth cookie """
    return HTTPFound(location=request.resource_url(request.context),
                     headers=forget(request))


@view_config(route_name='login', renderer='login.jinja2',
             permission=NO_PERMISSION_REQUIRED)
@view_config(context=HTTPForbidden, renderer='login.jinja2',
             permission=NO_PERMISSION_REQUIRED)
def do_login(context, request):
    """ Render the login form and handle the login action """
    if isinstance(context, HTTPForbidden):
        request.response.status_code = 403
    login_url = request.resource_url(request.context, 'login')
    referrer = request.url
    # never use the login form itself as came_from
    if referrer == login_url:
        referrer = _get_app_root(request)
    came_from = request.params.get('came_from', referrer)
    message = ''
    userid = ''
    password = ''
    if 'do_auth' in request.params:
        userid = request.param('userid')
        password = request.param('password')
        if request.registry.auth_db.authenticate(request, userid, password):
            headers = remember(request, userid)
            return HTTPFound(location=came_from,
                             headers=headers)
        message = 'Login failed'

    return {'message': message, 'came_from': came_from, 'userid': userid,
            'password': password, }
