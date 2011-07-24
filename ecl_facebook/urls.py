from django.conf.urls.defaults import *

urlpatterns = patterns('ecl_facebook.views',
    url(r'^begin$', 'facebook_oauth_begin', name='facebook-oauth-begin'),
    url(r'^complete$', 'facebook_oauth_complete', name='facebook-oauth-complete'),
)

