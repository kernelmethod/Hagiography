import secrets
from api.models.fields import TileField
from datetime import datetime, timezone
from django.db import models
from .user import User


def random_id():
    return secrets.token_urlsafe(8)


def current_time():
    return datetime.now(timezone.utc)


class GameRecord(models.Model):

    id = models.CharField(
        max_length=16,
        primary_key=True,
        default=random_id,
        null=False,
    )
    created = models.DateTimeField(default=current_time, null=False)

    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    game_mode = models.CharField(max_length=64, null=False)
    character_name = models.CharField(max_length=512, null=False)
    tile = TileField()
    score = models.BigIntegerField(null=False)
    turns = models.BigIntegerField(null=False)

    class Meta:
        indexes = [models.Index(fields=["id"]), models.Index(fields=["created"])]
