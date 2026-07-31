from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    notify = models.BooleanField(default=True)

    def __str__(self):
        return self.username


class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    meeting_time = models.DateTimeField()
    place = models.CharField(max_length=255, default="Центр")

    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='events',
        blank=True
    )

    def __str__(self):
        return self.name