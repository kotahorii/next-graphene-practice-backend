from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        User,
        related_name='profile',
        on_delete=models.CASCADE
    )
    followings = models.ManyToManyField(
        User, related_name='followings', blank=True
    )
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
