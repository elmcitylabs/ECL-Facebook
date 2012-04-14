.. ECL Facebook documentation master file, created by
   sphinx-quickstart on Thu Apr 12 12:18:30 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

ECL Facebook
===========

About
-----

ECL Facebook is an awesome Facebook library for Python 2.7+. It makes the Facebook
API a joy to use, and Django integration is baked in. To find out more, read
on!

If you have an issue to report or a feature request, add it at
https://github.com/elmcitylabs/ECL-Facebook/issues.

.. _installation:

Installation
------------

ECL Facebook is on PyPi, so we recommend installing via `pip`_ ::

    $ pip install ecl-twitter

.. _pip: http://www.pip-installer.org/en/latest/

.. _configuration:

Configuration
-------------

If you'd like to use ECL Facebook for a stand alone application (e.g., in a
script you're writing to download your tweets), you'll need to set the
environment variables ``FACEBOOK_KEY``, ``FACEBOOK_SECRET``,
``FACEBOOK_REDIRECT_URL``, and ``FACEBOOK_SCOPE`` with the values appropriate
for your Facebook application. ::

    export FACEBOOK_KEY="Gmxb5Rh7gpOpzunQ7SQcOA"
    export FACEBOOK_SECRET="irhZg1W5NO2r7M9IRwhjHKpzKPjJ3HXc6RYCbrM0"
    export FACEBOOK_REDIRECT_URL="http://example.com/oauth/complete"
    export FACEBOOK_SCOPE="email"

If you're only interested in integration with Django, read :ref:`django`.

.. _authentication:

Authentication
--------------

We've made authentication very simple. Probably too simple, to be honest.::

    >>> from ecl_facebook.settings import DIALOG_URL
    >>> DIALOG_URL
    https://www.facebook.com/dialog/oauth?scope=email&redirect_uri=http%3A%2F%2Fexample.com%2Fredirect&client_id=340516819320318

After opening this URL in your browser and allowing the application, you'll be redirected to a page with a URL similar to the following. ::

    http://local.goodiebag.elmcitylabs.com/redirect?code=AQDOvI5wqlwNXQ6AK9jepHW4LUKboJk7v9yLGeaFNCDCs1hchWpCYoqDF0FZFLS03YOZJ1lLhrzQrQ7PNWD2iiZZ6IBaW0KG6255_e3prYu60QZd6_IOIiC1z0U3w2SWJDiq_rtD0KQtcJk__YvZa1XSicZA5fnyEtEZBE3XzNpEgzp1fZZ8HEeQCrqazGjUNjU#_=_

Copy 

    >>> facebook = Facebook(token, secret)
    >>> data = twitter.oauth.access_token(oauth_verifier=verifier)
    >>> data
    <Objectifier#dict oauth_token_secret=unicode user_id=unicode oauth_token=unicode screen_name=unicode>

Congratulations, you have successfully authenticated with Facebook (told you it was easy). ``data`` is an ``Objectifier`` object which should contain your token, secret, user id, and screen name.

To call the API, use your newly-acquired access token and access token secret::

    >>> twitter = Facebook(data.oauth_token, data.oauth_token_secret)
    >>> tweets = twitter.statuses.user_timeline()
    >>> tweets
    <Objectifier#list elements:20>

So, yeah. That's it. Be fruitful and multiply.

.. _django:

Integrating with Django
-----------------------

What we did above is easy. For Django projects, we've made it even easier. In your views file::

    from django.contrib.auth import authenticate, login
    from django.http import HttpResponseRedirect

    from ecl_twitter import twitter_begin, twitter_callback

    from .models import User

    # ...

    @twitter_begin
    def oauth_twitter_begin(request):
        pass

    @twitter_callback
    def oauth_twitter_complete(request, data):
        user, _ = User.objects.get_or_create(screen_name=data.screen_name, defaults={
            'access_token': data.oauth_token,
            'access_token_secret': data.oauth_token_secret })
        user = authenticate(id=user.id)
        login(request, user)
        return HttpResponseRedirect(reverse('home'))

Add these values to your settings.::

    # The User model that you'll be using to authenticate with Facebook.
    PRIMARY_USER_MODEL = "app.User"

    AUTHENTICATION_BACKENDS = (
        # ...
        'ecl_twitter.backends.FacebookAuthBackend',
    )

    TWITTER_KEY = "Gmxb5Rh7gpOpzunQ7SQcOA"
    TWITTER_SECRET = "irhZg1W5NO2r7M9IRwhjHKpzKPjJ3HXc6RYCbrM0"
    TWITTER_REDIRECT_URL = "http://example.com/oauth/complete"

Then map the above views in your urls.py::

    # ...

    urlpatterns = patterns('app.views',
        # ...
        url(r'^oauth/twitter/begin$', 'oauth_twitter_begin'),
        url(r'^oauth/twitter/complete$', 'oauth_twitter_complete'),
    )

You're done. Oh, you might also want to add some fields for storing the
Facebook-related fields in your user model.

Contributing, feedback, and questions
-------------------------------------

* Github: https://github.com/elmcitylabs
* Email: opensource@elmcitylabs.com.
* Twitter: `@elmcitylabs <http://twitter.com/elmcitylabs>`_

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

