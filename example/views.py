from django.http import HttpResponse

from ecl_facebook.decorators import facebook_begin
from ecl_facebook.decorators import facebook_callback
from ecl_facebook.facebook import Facebook

def home(request):
    return HttpResponse("See '/oauth/facebook/begin'")

@facebook_begin
def oauth_facebook_begin(request):
    return {}

@facebook_callback
def oauth_facebook_complete(request, token):
    fb = Facebook(token)
    user = fb.me()
    return HttpResponse("Hello, {}!".format(user.name))

