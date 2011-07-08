from django.http import HttpResponseRedirect
from django.views.decorators.http import require_GET
from django.conf import settings
from django.core.urlresolvers import reverse
import urllib
import cgi
import facebook

FACEBOOK_OAUTH_DIALOG_PARAMS = {
        "client_id": settings.FACEBOOK_APP_ID,
        "redirect_uri": settings.FACEBOOK_REDIRECT_URI,
        "scope": settings.FACEBOOK_OAUTH_SCOPE
    }

FACEBOOK_ACCESS_TOKEN_PARAMS = {
    "client_id": settings.FACEBOOK_APP_ID,
    "client_secret": settings.FACEBOOK_APP_SECRET,
    "redirect_uri": settings.FACEBOOK_REDIRECT_URI,
}

FACEBOOK_OAUTH_DIALOG_URL = "https://www.facebook.com/dialog/oauth?" + urllib.urlencode(FACEBOOK_OAUTH_DIALOG_PARAMS)

@require_GET
def facebook_oauth_begin(request):
    return HttpResponseRedirect(FACEBOOK_OAUTH_DIALOG_URL)

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

    access_token = attributes['access_token'][0]

    graph = facebook.GraphAPI(access_token)
    profile = graph.get_object("me")

    id = profile['id']

    if request.user.is_authenticated() and not request.user.facebook_id:
        graph = facebook.GraphAPI(access_token)
        friends = graph.get_connections('me', 'friends')
        friend_ids = ','.join(map(lambda k: k['id'], friends['data']))

        user = request.user
        user.facebook_id = id
        user.facebook_access_token = access_token
        user.facebook_friends = friend_ids
        user.save()

        # The user now has Facebook data. Redirect them where appropriate.
        if 'redirect_to_pledge' in request.session:
            pledge_id = request.session['redirect_to_pledge']
            return HttpResponseRedirect(reverse('view-pledge', args=[pledge_id]))
        else:
            return HttpResponseRedirect(reverse('home'))
    else:
        raise Exception, "Not implemented"

