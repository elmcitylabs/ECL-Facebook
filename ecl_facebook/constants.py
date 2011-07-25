from django.conf import settings
import urllib

FACEBOOK_DIALOG_PARAMS = {
        'client_id': settings.FACEBOOK_KEY,
        'redirect_uri': settings.FACEBOOK_REDIRECT_URL,
        'scope': settings.FACEBOOK_SCOPE
    }

FACEBOOK_ACCESS_TOKEN_PARAMS = {
    'client_id': settings.FACEBOOK_KEY,
    'client_secret': settings.FACEBOOK_SECRET,
    'redirect_uri': settings.FACEBOOK_REDIRECT_URL,
}

FACEBOOK_DIALOG_URL = "https://www.facebook.com/dialog/oauth?" + urllib.urlencode(FACEBOOK_DIALOG_PARAMS)
try:
    FACEBOOK_POST_COMPLETE_URL = settings.FACEBOOK_POST_COMPLETE_URL
except:
    FACEBOOK_POST_COMPLETE_URL = "/"

