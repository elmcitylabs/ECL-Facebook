from django.conf.urls.defaults import *

urlpatterns = patterns('ecl_facebook.views',
    url(r'^begin$', 'facebook_oauth_begin', name='facebook-oauth-begin'),
)

