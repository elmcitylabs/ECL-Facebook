from django.http import HttpResponseRedirect
from django.views.decorators.http import require_GET
from decorators import facebook_callback
import constants

@require_GET
def facebook_oauth_begin(request):
    return HttpResponseRedirect(constants.FACEBOOK_DIALOG_URL)

@require_GET
@facebook_callback
def facebook_oauth_complete(request, token, id):
    return HttpResponseRedirect(constants.FACEBOOK_POST_COMPLETE_URL)

