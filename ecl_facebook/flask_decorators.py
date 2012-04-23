from flask import session, redirect, request
from functools import wraps
import urllib
import uuid
import django

from django.http import HttpResponseRedirect

from ecl_facebook.facebook import Facebook, FacebookError
from ecl_facebook.settings import DIALOG_URL, DIALOG_PARAMS, CSRF_TOKEN_REQUIRED

def facebook_begin(fun_or_app, route=None):
    def handler(fun, *args, **kwargs):
        params = DIALOG_PARAMS.copy()
        if CSRF_TOKEN_REQUIRED:
            state = str(uuid.uuid4())
            params['state'] = state
            session['facebook_state'] = state
        return redirect("{}?{}".format(DIALOG_URL, urllib.urlencode(params)))

    if route is None:
        fun = fun_or_app
        inner = lambda *args, **kwargs: handler(fun, *args, **kwargs)
        inner = wraps(fun)(inner)
        return inner
    else:
        app = fun_or_app
        def decorator(fun):
            inner = lambda *args, **kwargs: handler(fun, *args, **kwargs)
            inner = wraps(fun)(inner)
            app.add_url_rule(route, None, inner)
            return inner
        return decorator

def facebook_callback(fun_or_app, route=None):
    def handler(fun, *args, **kwargs):
        error = None
        access_token = None
        if CSRF_TOKEN_REQUIRED:
            if 'state' not in request.args:
                error = FacebookError(message="`state` parameter is required. This request might have been initiated by an unauthorized third-party.", err="StateMissing")
            elif session['facebook_state'] != request.args['state']:
                error = FacebookError(message="`state` parameter does not match session value. This request might have been initiated by an unauthorized third-party.", err="StateMismatch")
            del session['facebook_state']
        elif 'error' in request.args:
            message = request.args.get('error_description')
            err = request.args.get('error')
            reason = request.args.get('error_reason')
            error = FacebookError(message=message, err=err, code=reason)
        elif 'code' not in request.args:
            error = FacebookError(message="`code` is a required parameter.", err="CodeMissing")

        if error is None:
            code = request.args.get('code')
            facebook = Facebook()
            response = facebook.oauth.access_token(code=code)
            try:
                access_token = response.access_token
            except AttributeError:
                access_token = response['access_token']

            from ecl_facebook.signals import post_facebook_auth
            post_facebook_auth.send('ecl_facebook', token=access_token)

        return fun(access_token, error)

    if route is None:
        fun = fun_or_app
        inner = lambda *args, **kwargs: handler(fun, *args, **kwargs)
        inner = wraps(fun)(inner)
        return inner
    else:
        app = fun_or_app
        def decorator(fun):
            inner = lambda *args, **kwargs: handler(fun, *args, **kwargs)
            inner = wraps(fun)(inner)
            app.add_url_rule(route, None, inner)
            return inner
        return decorator

