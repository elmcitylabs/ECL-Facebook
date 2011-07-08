from django.dispatch import Signal

facebook_auth_started = Signal(providing_args=[])
facebook_auth_completed = Signal(providing_args=['access_token', \
        'access_token_secret', 'username', 'id'])

