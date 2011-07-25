from django.dispatch import Signal

post_facebook_auth = Signal(providing_args=['token'])

