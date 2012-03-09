from __future__ import print_function

import webbrowser

from django.test import TestCase

from ecl_facebook import settings
from ecl_facebook.facebook import Facebook

from .models import User
from .views import oauth_facebook_complete

class FacebookTest(TestCase):
    def test_desktop_app_callback(self):
        print("Redirecting web browser to desktop dialog URL...")
        webbrowser.open_new_tab(settings.DESKTOP_DIALOG_URL)
        access_token = raw_input("Enter the access token: ")
        fb = Facebook(access_token)
        user = fb.me()
        self.assertIsNotNone(user.email)

    def test_web_app_callback(self):
        print("Redirecting web browser to dialog URL...")
        webbrowser.open_new_tab(settings.DIALOG_URL)
        get_params = raw_input("Enter the GET parameters: ")
        response = self.client.get('/oauth/facebook/complete?{}'.format(get_params))
        access_token = response.content
        fb = Facebook(access_token)
        user = fb.me()
        self.assertIsNotNone(user.email)

