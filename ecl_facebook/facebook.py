import json
import urllib2
import urllib

FACEBOOK_API_BASE = "https://graph.facebook.com/"

class Objectifier(object):
    def __init__(self, response_data):
        self.response_data = response_data

    @staticmethod
    def objectify_if_needed(response_data):
        if type(response_data) in [dict, list]:
            return Objectifier(response_data)
        return response_data

    def __repr__(self):
        if type(self.response_data) == dict:
            return "<Objectifier#dict %s>" % " ".join(["%s=%s" % (k, type(v).__name__) for k, v in self.response_data.iteritems()])
        elif type(self.response_data) == list:
            return "<Objectifier#list elements:%d>" % len(self.response_data)
        else:
            return self.response_data

    def __contains__(self, k):
        if type(self.response_data) in [dict, list]:
            return k in self.response_data
        return False

    def __len__(self):
        return len(self.response_data)

    def __iter__(self):
        if type(self.response_data) == dict:
            for k, v in self.response_data.iteritems():
                yield (k, Objectifier.objectify_if_needed(v))
        elif type(self.response_data) == list:
            for i in self.response_data:
                yield Objectifier.objectify_if_needed(i)
        else:
            raise StopIteration

    def __getitem__(self, k):
        if type(self.response_data) == dict and k in self.response_data:
            return Objectifier.objectify_if_needed(self.response_data[k])
        elif type(self.response_data) == list and k <= len(self.response_data):
            return Objectifier.objectify_if_needed(self.response_data[k])
        return None

    def __getattr__(self, k):
        if k in self.response_data:
            return Objectifier.objectify_if_needed(self.response_data[k])
        return None


class FacebookError(Exception):
    def __init__(self, message, type, code):
        self.message = message
        self.type = type
        self.code = code

    def __str__(self):
        return "%s (%s), %s" % (self.type, self.code, self.message)


class FacebookCall(object):
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
        kwargs['access_token'] = self.token

        # Format dats with Unix timestamps instead of ISO-8601.
        kwargs['date_format'] = 'U'
        encoded_params = urllib.urlencode(kwargs)

        url = FACEBOOK_API_BASE + endpoint
        if method == 'GET':
            url += "?" + encoded_params
            request = urllib2.Request(url)
        else:
            request = urllib2.Request(url, encoded_params)

        try:
            response = urllib2.urlopen(request)
        except urllib2.HTTPError, e:
            data = json.load(e)
            type = data['error']['type']
            message = data['error']['message']
            raise FacebookError(message=message, type=type, code=e.code)

        data = response.read()
        try:
            response_obj = Objectifier(json.loads(data))
        except ValueError:
            return data

        if 'error' in response_obj:
            raise FacebookError(message=response_obj.error.message,
                    type=response_obj.error.type, code=response.code)

        return response_obj


class Facebook(object):
    def __init__(self, token):
        """
        Example Usage

        >>> facebook = Facebook("3JUBENXURSR0RJNWOBQBTSNTBCQHQKOZW2USJYF25BXNXEMC")
        >>> facebook.me()
        >>> facebook.me.checkins()
        """
        self.token = token

    def __getattr__(self, k):
        return FacebookCall(self.token, [k])


