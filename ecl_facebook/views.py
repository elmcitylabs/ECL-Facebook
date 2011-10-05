from django.http import HttpResponseRedirect
from django.views.decorators.http import require_GET
from decorators import facebook_callback
import constants

@require_GET
def oauth_facebook_begin(request):
    if 'popup' in request.GET:
        request.session['facebook_popup'] = True

    return HttpResponseRedirect(constants.FACEBOOK_DIALOG_URL)

@require_GET
@facebook_callback
def oauth_facebook_complete(request, token, id):
    return HttpResponseRedirect(constants.FACEBOOK_REDIRECT_URL)

