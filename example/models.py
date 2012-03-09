from django.db import models

class User(models.Model):
    facebook_id = models.CharField(max_length=32, blank=True, null=True,
            unique=True, db_index=True)
    facebook_token = models.CharField(max_length=128, blank=True, null=True)

    def is_authenticated(self):
        return True

