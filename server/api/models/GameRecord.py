import secrets
from datetime import datetime
from django.db import models


class GameRecord(models.Model):

    id = models.CharField(
        max_length=16,
        primary_key=True,
        default=lambda: secrets.token_urlsafe(8),
        null=False,
    )
    created = models.DateTimeField(default=datetime.utcnow, null=False)

    game_mode = models.CharField(max_length=64, null=False)
    character_name = models.CharField(max_length=512, null=False)
    tile = models.CharField(max_length=256, null=False)
    score = models.BigIntegerField(null=False)
    turns = models.BigIntegerField(null=False)

    class Meta:
        indexes = [models.Index(fields=["id"]), models.Index(fields=["created"])]
