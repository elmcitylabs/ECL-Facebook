from django.conf import settings
import urllib

KEY = getattr(settings, 'FACEBOOK_KEY', None)
SECRET = getattr(settings, 'FACEBOOK_SECRET', None)
REDIRECT_URL = getattr(settings, 'FACEBOOK_REDIRECT_URL', None)
SCOPE = getattr(settings, 'FACEBOOK_SCOPE', None)

if not all([KEY, SECRET, REDIRECT_URL, SCOPE]):
    raise ImportError("FACEBOOK_KEY, FACEBOOK_SECRET, FACEBOOK_REDIRECT_URL, \
            and FACEBOOK_SCOPE must all be defined in your settings.py file.")

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

