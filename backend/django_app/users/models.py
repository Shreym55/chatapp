from django.contrib.auth.models import AbstractUser
from django.db import models

def avatar_path(instance, filename):
    return f'avatars/user_{instance.id}/{filename}'

class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to=avatar_path, blank=True, null=True)
    status = models.CharField(max_length=100, default="Hey there! I am using Echo")
    def __str__(self):
        return self.username