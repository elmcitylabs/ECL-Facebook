Installation
============

    pip install ecl_facebook

In your "settings.py" file, set values for `FACEBOOK_KEY`, `FACEBOOK_SECRET`,
`FACEBOOK_REDIRECT_URL`, and `FACEBOOK_SCOPE`.


    FACEBOOK_KEY = "340516819320318"
    FACEBOOK_SECRET = "36388212bada9111d9e59a6889f49738"
    FACEBOOK_REDIRECT_URL = "http://google.com/oauth/facebook/complete"
    FACEBOOK_SCOPE = "email,publish_stream"

If you want to be sent a signal when the user authorizes the app, also add
`ecl_facebook` to your `INSTALLED_APPS`.

Then, in your views, use the decorators `@facebook_begin` and `@facebook_callback` to start and complete the Facebook authentication flow, respectively.

    from ecl_facebook.decorators import facebook_begin, facebook_callback

    @facebook_begin
    def oauth_facebook_begin(request):
        # This view will redirect to the appropriate Facebook authentication URL
        return {}

    @facebook_callback
    def oauth_facebook_complete(request, token):
        # `token` contains the Facebook access token you can use to access your
        # users' information
        return {}

Finally, set up these views in your "urls.py".

    from django.conf.urls.defaults import patterns, url
    from myapp import views

    urlpatterns = patterns('',
        url(r'^oauth/facebook/begin$', views.oauth_facebook_begin),
        url(r'^oauth/facebook/complete$', views.oauth_facebook_complete),
    )


