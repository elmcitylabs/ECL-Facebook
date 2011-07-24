from django.http import HttpResponseRedirect
from django.views.decorators.http import require_GET
from django.conf import settings
import urllib
import cgi
from signals import post_facebook_auth

FACEBOOK_DIALOG_PARAMS = {
        "client_id": settings.FACEBOOK_KEY,
        "redirect_uri": settings.FACEBOOK_REDIRECT_URL,
        "scope": settings.FACEBOOK_SCOPE
    }

FACEBOOK_ACCESS_TOKEN_PARAMS = {
    "client_id": settings.FACEBOOK_KEY,
    "client_secret": settings.FACEBOOK_SECRET,
    "redirect_uri": settings.FACEBOOK_REDIRECT_URL,
}

FACEBOOK_DIALOG_URL = "https://www.facebook.com/dialog/oauth?" + urllib.urlencode(FACEBOOK_DIALOG_PARAMS)

@require_GET
def facebook_oauth_begin(request):
    return HttpResponseRedirect(FACEBOOK_DIALOG_URL)

@require_GET
def facebook_oauth_complete(request):
    code = request.GET['code']

    params = FACEBOOK_ACCESS_TOKEN_PARAMS.copy()
    params['code'] = code
    url = "https://graph.facebook.com/oauth/access_token?" + urllib.urlencode(params)

    # Fetch the access token
    response = urllib.urlopen(url)
    data = response.read()
    attributes = cgi.parse_qs(data)

    token = attributes['access_token'][0]

    post_facebook_auth.send("ecl_facebook", token=token, id=request.user.id)

    return HttpResponseRedirect(settings.FACEBOOK_POST_COMPLETE_URL)

