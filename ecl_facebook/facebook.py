import base64
import cgi
import hashlib
import hmac
import json
import time
import urllib
import urllib2

from objectifier import Objectifier

import settings

API_BASE = "https://graph.facebook.com/"

class FacebookError(Exception):
    """
    Exception for all Facebook Graph API-related errors.
    """
    def __init__(self, message, err, code=None):
        self.message = message
        self.err = err
        self.code = code

    def __str__(self):
        if self.code is None:
            return "{}, {}".format(self.err, self.message)
        else:
            return "{} ({}), {}".format(self.err, self.code, self.message)


class FacebookCall(object):
    """
    Abstract object that helps create a clean object-based interface to the
    Facebook Graph API.
    """
    def __init__(self, token, endpoint_components):
        self.token = token
        self.endpoint_components = endpoint_components

    def __getattr__(self, k):
        self.endpoint_components.append(k)
        return FacebookCall(self.token, self.endpoint_components)

    def __getitem__(self, k):
        self.endpoint_components.append(str(k))
        return FacebookCall(self.token, self.endpoint_components)

    def __call__(self, method='GET', **kwargs):
        endpoint = "/".join(self.endpoint_components)

        if self.token is None:
            kwargs.update(settings.ACCESS_TOKEN_PARAMS)
        else:
            kwargs['access_token'] = self.token

        # Format dats with Unix timestamps instead of ISO-8601.
        # kwargs['date_format'] = 'U'
        encoded_params = urllib.urlencode(kwargs)

        url = API_BASE + endpoint
        if method == 'GET':
            url += "?" + encoded_params
            request = urllib2.Request(url)
        else:
            request = urllib2.Request(url, encoded_params)

        try:
            response = urllib2.urlopen(request)
        except urllib2.HTTPError, e:
            data = json.load(e)
            err = data['error']['type']
            message = data['error']['message']
            raise FacebookError(message=message, err=err, code=e.code)

        data = response.read()

        if 'text/plain' in response.headers['content-type']:
            return Objectifier(cgi.parse_qsl(data))

        try:
            response_obj = Objectifier(data)
        except ValueError:
            return data

        if 'error' in response_obj:
            raise FacebookError(message=response_obj.error.message,
                    err=response_obj.error.type, code=response.code)

        return response_obj


class Facebook(object):
    """
    Example Usage

    >>> facebook = Facebook("3JUBENXURSR0RJNWOBQBTSNTBCQHQKOZW2USJYF25BXNXEMC")
    >>> facebook.me()
    >>> facebook.me.checkins()
    """

    def __init__(self, token=None):
        self.token = token

    def __getitem__(self, k):
        return FacebookCall(self.token, [k])

    def __getattr__(self, k):
        return FacebookCall(self.token, [k])


def get_user_from_cookie(cookies, app_id, app_secret):
    """Parses the cookie set by the official Facebook JavaScript SDK.

    cookies should be a dictionary-like object mapping cookie names to
    cookie values.

    If the user is logged in via Facebook, we return a dictionary with the
    keys "uid" and "access_token". The former is the user's Facebook ID,
    and the latter can be used to make authenticated requests to the Graph API.
    If the user is not logged in, we return None.

    Download the official Facebook JavaScript SDK at
    http://github.com/facebook/connect-js/. Read more about Facebook
    authentication at http://developers.facebook.com/docs/authentication/.
    """
    cookie = cookies.get("fbs_" + app_id, "")
    if not cookie: return None
    args = dict((k, v[-1]) for k, v in cgi.parse_qs(cookie.strip('"')).items())
    payload = "".join(k + "=" + args[k] for k in sorted(args.keys())
                      if k != "sig")
    sig = hashlib.md5(payload + app_secret).hexdigest()
    expires = int(args["expires"])
    if sig == args.get("sig") and (expires == 0 or time.time() < expires):
        return args
    else:
        return None

def parse_signed_request(signed_request, app_secret):
    """ Return dictionary with signed request data.

    We return a dictionary containing the information in the signed_request. This will
    include a user_id if the user has authorised your application, as well as any
    information requested in the scope.

    If the signed_request is malformed or corrupted, False is returned.
    """
    try:
        l = signed_request.split('.', 2)
        encoded_sig = str(l[0])
        payload = str(l[1])
        sig = base64.urlsafe_b64decode(encoded_sig + "=" * ((4 - len(encoded_sig) % 4) % 4))
        data = base64.urlsafe_b64decode(payload + "=" * ((4 - len(payload) % 4) % 4))
    except IndexError:
        return False # raise ValueError('signed_request malformed')
    except TypeError:
        return False # raise ValueError('signed_request had corrupted payload')

    data = json.loads(data)
    if data.get('algorithm', '').upper() != 'HMAC-SHA256':
        return False # raise ValueError('signed_request used unknown algorithm')

    expected_sig = hmac.new(app_secret, msg=payload, digestmod=hashlib.sha256).digest()
    if sig != expected_sig:
        return False # raise ValueError('signed_request had signature mismatch')

    return data

def auth_url(app_id, canvas_url, perms = None):
    url = "https://www.facebook.com/dialog/oauth?"
    kvps = {'client_id': app_id, 'redirect_uri': canvas_url}
    if perms:
        kvps['scope'] = ",".join(perms)
    return url + urllib.urlencode(kvps)

def get_app_access_token(application_id, application_secret):
    """
    Get the access_token for the app that can be used for insights and creating test users
    application_id = retrieved from the developer page
    application_secret = retrieved from the developer page
    returns the application access_token
    """
    # Get an app access token
    args = {'grant_type':'client_credentials',
            'client_id':application_id,
            'client_secret':application_secret}

    file = urllib2.urlopen("https://graph.facebook.com/oauth/access_token?" +
                              urllib.urlencode(args))

    try:
        result = file.read().split("=")[1]
    finally:
        file.close()

    return result


