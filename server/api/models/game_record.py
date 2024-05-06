import secrets
from datetime import datetime, timezone
from django.db import models


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

    game_mode = models.CharField(max_length=64, null=False)
    character_name = models.CharField(max_length=512, null=False)
    tile = models.CharField(max_length=256, null=False)
    score = models.BigIntegerField(null=False)
    turns = models.BigIntegerField(null=False)

    class Meta:
        indexes = [models.Index(fields=["id"]), models.Index(fields=["created"])]
