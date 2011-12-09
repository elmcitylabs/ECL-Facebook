import cgi
import urllib

from signals import post_facebook_auth
import constants

def facebook_callback(fun):
    def k(request, *args, **kwargs):
        code = request.GET.get('code', None)
        if not code:
            # XXX Incorporate better app-specific error handling here.
            return HttpResponse("'code' is a required parameter.")

        params = constants.FACEBOOK_ACCESS_TOKEN_PARAMS.copy()
        params['code'] = code
        url = "https://graph.facebook.com/oauth/access_token?" + urllib.urlencode(params)

        # Fetch the access token
        response = urllib.urlopen(url)
        data = response.read()
        attributes = cgi.parse_qs(data)

        token = attributes['access_token'][0]

        post_facebook_auth.send('ecl_facebook', token=token)

        return fun(request, token, *args, **kwargs)
    return k

