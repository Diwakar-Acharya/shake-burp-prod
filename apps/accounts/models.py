from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    google_id = models.CharField(max_length=255, blank=True, null=True, unique=True)

    def __str__(self) -> str:
        return str(self.username)
