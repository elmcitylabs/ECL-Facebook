#!/usr/bin/env python

from __future__ import print_function

import sys

from optparse import OptionParser
from django.conf import settings

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('-k', "--key", dest='FACEBOOK_KEY', type=str)
    parser.add_option('-s', "--secret", dest='FACEBOOK_SECRET', type=str)
    parser.add_option('-r', "--redirect", dest='FACEBOOK_REDIRECT_URL',
            type=str, default="http://localhost:8000/oauth/facebook/complete")
    parser.add_option('--scope', dest='FACEBOOK_SCOPE', type=str, default="email")
    options, args = parser.parse_args()

    if not options.FACEBOOK_KEY:
        print("Missing parameter, see 'python runtests -h'.")
        sys.exit(0)

    if not options.FACEBOOK_SECRET:
        print("Missing parameter, see 'python runtests -h'.")
        sys.exit(0)

    settings.configure(
        INSTALLED_APPS=(
            "example",
        ),
        ROOT_URLCONF="example.urls",
        FACEBOOK_KEY=options.FACEBOOK_KEY,
        FACEBOOK_SECRET=options.FACEBOOK_SECRET,
        FACEBOOK_REDIRECT_URL=options.FACEBOOK_REDIRECT_URL,
        FACEBOOK_SCOPE=options.FACEBOOK_SCOPE,
        AUTHENTICATION_BACKENDS=(
            "example.backends.FBAuthBackend",
        ),
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": ":memory:",
            }
        },
    )

    from django.core.management import call_command
    call_command("test", "example")

