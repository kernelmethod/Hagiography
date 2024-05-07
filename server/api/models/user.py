from datetime import datetime, timezone
from django.contrib.auth.models import AbstractUser
from django.db import models


def current_time():
    return datetime.now(timezone.utc)


class User(AbstractUser):

    id = models.AutoField(primary_key=True)

    email = models.EmailField(unique=True, null=False)
    username = models.CharField(max_length=64, unique=True, null=False)
    password = models.CharField(max_length=256, null=False)
    created = models.DateTimeField(default=current_time, null=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
