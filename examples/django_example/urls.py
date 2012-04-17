from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('examples.django_example.views',
    url(r'^$', 'home', name=''),
    url(r'^oauth/facebook/begin$', 'oauth_facebook_begin', name='oauth-facebook-begin'),
    url(r'^oauth/facebook/complete$', 'oauth_facebook_complete', name='oauth-facebook-complete'),
)
