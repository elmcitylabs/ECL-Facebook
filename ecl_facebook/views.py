from django.http import HttpResponseRedirect
from django.views.decorators.http import require_GET

from ecl_facebook.decorators import facebook_callback
from ecl_facebook import settings

@require_GET
def oauth_facebook_begin(request):
    """
    View that redirects the user to Facebook to authorize the application.
    """
    if 'popup' in request.GET:
        request.session['facebook_popup'] = True

    return HttpResponseRedirect(settings.DIALOG_URL)

@require_GET
@facebook_callback
def oauth_facebook_complete(request, token, error):
    """
    Sample view that shows how the `facebook_callback` decorator should be
    used.
    """
    return HttpResponseRedirect(settings.REDIRECT_URL)

