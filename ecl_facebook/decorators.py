from functools import wraps
import cgi
import urllib

from django.http import HttpResponseRedirect

from facebook import Facebook
import settings

def facebook_begin(fun):
    """
    Django view decorator that redirects the user to a URL where they can
    authorize the application.
    """
    @wraps(fun)
    def inner(request, *args, **kwargs):
        fun(request, *args, **kwargs)
        return HttpResponseRedirect(settings.DIALOG_URL)
    return inner

def facebook_callback(fun):
    """
    Decorator for views that generates an Graph API access token after a user
    authorizes the application on Facebook.

    The wrapped view is given three parameters: the original `request`
    parameter, the access token (`token`), and the Facebook id of the user who
    authenticated (`id`).
    """
    @wraps(fun)
    def inner(request, *args, **kwargs):
        code = request.GET.get('code')
        if not code:
            # TODO Incorporate better error handling.
            raise Exception("Cookies must be enabled to log in with Facebook.")

        params = settings.ACCESS_TOKEN_PARAMS.copy()
        params['code'] = code

        facebook = Facebook()
        response = facebook.oauth.access_token(**params)

        from .signals import post_facebook_auth
        post_facebook_auth.send('ecl_facebook', token=response.access_token)
        return fun(request, access_token, *args, **kwargs)
    return inner

