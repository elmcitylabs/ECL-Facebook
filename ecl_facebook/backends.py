from django.conf import settings
from django.db.models import get_model

app_label, model_name = settings.PRIMARY_USER_MODEL.split('.')
GenericUser = get_model(app_label, model_name)

class FacebookAuthBackend(object):
    def authenticate(self, id):
        try:
            return GenericUser.objects.get(id=id)
        except GenericUser.DoesNotExist:
            return None

    def get_user(self, id):
        try:
            return GenericUser.objects.get(pk=id)
        except GenericUser.DoesNotExist:
            return None


