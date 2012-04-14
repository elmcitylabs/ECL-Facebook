from django.http import HttpResponse

from ecl_facebook import facebook_begin
from ecl_facebook import facebook_callback
from ecl_facebook import Facebook

def home(request):
    return HttpResponse("See '/oauth/facebook/begin'")

@facebook_begin
def oauth_facebook_begin(request):
    return {}

@facebook_callback
def oauth_facebook_complete(request, token):
    return HttpResponse(token)

