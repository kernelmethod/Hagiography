from django.db import models
from .game_record import GameRecord


class JournalAccomplishment(models.Model):

    game_record = models.ForeignKey(GameRecord, on_delete=models.CASCADE)

    time = models.BigIntegerField(null=False)
    text = models.CharField(max_length=1024, null=False)
    snapshot = models.CharField(max_length=96 * 5 * 9)
