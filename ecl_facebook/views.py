from django.http import HttpResponseRedirect
from django.views.decorators.http import require_GET
from django.conf import settings
from django.core.urlresolvers import reverse
import urllib
import cgi
import facebook

FACEBOOK_DIALOG_PARAMS = {
        "client_id": settings.FACEBOOK_APP_ID,
        "redirect_uri": settings.FACEBOOK_REDIRECT_URL,
        "scope": settings.FACEBOOK_SCOPE
    }

FACEBOOK_ACCESS_TOKEN_PARAMS = {
    "client_id": settings.FACEBOOK_APP_ID,
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

    return HttpResponseRedirect("%s?token=%s" % (reverse(settings.FACEBOOK_POST_COMPLETE_URL), token))

