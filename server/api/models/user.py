from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    email = models.EmailField(primary_key=True, unique=True, null=False)
    username = models.CharField(max_length=64, unique=True, null=False)
    password = models.CharField(max_length=256, null=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
