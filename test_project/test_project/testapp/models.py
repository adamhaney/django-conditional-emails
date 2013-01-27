from django.db import models
from django.contrib.auth.models import User

class UserProperty(models.Model):
    some_char = models.CharField(max_length=37)
    some_time = models.DateTimeField()
    user = models.ForeignKey(User, related_name='test_user_property')

