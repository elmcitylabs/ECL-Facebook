from .models import User

class FBAuthBackend():
    def authenticate(self, facebook_id):
        try:
            user = User.objects.get(facebook_id=facebook_id)
        except User.DoesNotExist:
            return None
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

