from django.http import HttpResponse

from ecl_facebook.decorators import django
from ecl_facebook import Facebook

def home(request):
    return HttpResponse("See '/oauth/facebook/begin'")

@django.facebook_begin
def oauth_facebook_begin(request):
    return {}

@django.facebook_callback
def oauth_facebook_complete(request, token, error):
    return HttpResponse(token)

