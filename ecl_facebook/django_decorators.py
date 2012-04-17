from functools import wraps
import urllib
import uuid
import django

from django.http import HttpResponseRedirect

from ecl_facebook.facebook import Facebook, FacebookError
from ecl_facebook.settings import DIALOG_URL, DIALOG_PARAMS, CSRF_TOKEN_REQUIRED

def facebook_begin(fun):
    """
    Django view decorator that redirects the user to a URL where they can
    authorize the application.
    """
    @wraps(fun)
    def inner(request, *args, **kwargs):
        fun(request, *args, **kwargs)
        params = DIALOG_PARAMS.copy()
        if CSRF_TOKEN_REQUIRED:
            state = str(uuid.uuid4())
            params['state'] = state
            request.session['facebook_state'] = state
        return HttpResponseRedirect("{}?{}".format(DIALOG_URL, urllib.urlencode(params)))
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
        error = None
        access_token = None
        if CSRF_TOKEN_REQUIRED:
            if 'state' not in request.GET:
                error = FacebookError(message="`state` parameter is required. This request might have been initiated by an unauthorized third-party.", err="StateMissing")
            elif request.session['facebook_state'] != request.GET['state']:
                error = FacebookError(message="`state` parameter does not match session value. This request might have been initiated by an unauthorized third-party.", err="StateMismatch")
            del request.session['facebook_state']
        elif 'error' in request.GET:
            message = request.GET.get('error_description')
            err = request.GET.get('error')
            reason = request.GET.get('error_reason')
            error = FacebookError(message=message, err=err, code=reason)
        elif 'code' not in request.GET:
            error = FacebookError(message="`code` is a required parameter.", err="CodeMissing")

        if error is None:
            code = request.GET.get('code')
            facebook = Facebook()
            response = facebook.oauth.access_token(code=code)
            access_token = response.access_token
            from ecl_facebook.signals import post_facebook_auth
            post_facebook_auth.send('ecl_facebook', token=access_token)

        return fun(request, access_token, error, *args, **kwargs)
    return inner

