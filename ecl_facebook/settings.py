try:
    from django.conf import settings
    dir(settings)
except ImportError:
    import os
    class settings(object):
        FACEBOOK_KEY = os.environ.get('FACEBOOK_KEY')
        FACEBOOK_SECRET = os.environ.get('FACEBOOK_SECRET')
        FACEBOOK_REDIRECT_URL = os.environ.get('FACEBOOK_REDIRECT_URL')
        FACEBOOK_SCOPE = os.environ.get('FACEBOOK_SCOPE')
        FACEBOOK_CSRF_TOKEN_REQUIRED = os.environ.get('FACEBOOK_CSRF_TOKEN_REQUIRED') == '1'

import warnings
import urllib

KEY = getattr(settings, 'FACEBOOK_KEY', None)
SECRET = getattr(settings, 'FACEBOOK_SECRET', None)
REDIRECT_URL = getattr(settings, 'FACEBOOK_REDIRECT_URL', None)
SCOPE = getattr(settings, 'FACEBOOK_SCOPE', None)
CSRF_TOKEN_REQUIRED = getattr(settings, 'FACEBOOK_CSRF_TOKEN_REQUIRED', True)

if not all([KEY, SECRET, REDIRECT_URL, SCOPE]):
    warnings.warn("FACEBOOK_KEY, FACEBOOK_SECRET, FACEBOOK_REDIRECT_URL, and FACEBOOK_SCOPE must all be defined in your settings.py file or in your environment.", ImportWarning)

DIALOG_PARAMS = {
    'client_id': KEY,
    'redirect_uri': REDIRECT_URL,
    'scope': SCOPE
}

DESKTOP_DIALOG_PARAMS = {
    'client_id': KEY,
    'redirect_uri': "https://www.facebook.com/connect/login_success.html",
    'response_type': "token",
    'scope': SCOPE
}

ACCESS_TOKEN_PARAMS = {
    'client_id': KEY,
    'client_secret': SECRET,
    'redirect_uri': REDIRECT_URL
}

DIALOG_URL = "https://www.facebook.com/dialog/oauth?" + urllib.urlencode(DIALOG_PARAMS)

DESKTOP_DIALOG_URL = "https://www.facebook.com/dialog/oauth?" + \
        urllib.urlencode(DESKTOP_DIALOG_PARAMS)

