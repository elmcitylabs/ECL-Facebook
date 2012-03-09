from django.http import HttpResponse

from ecl_facebook.decorators import facebook_begin
from ecl_facebook.decorators import facebook_callback

def home(request):
    return HttpResponse("Hello")

@facebook_begin
def oauth_facebook_begin(request):
    return {}

@facebook_callback
def oauth_facebook_complete(request, token):
    return HttpResponse(token)

