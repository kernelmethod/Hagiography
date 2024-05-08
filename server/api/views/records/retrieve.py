from api import models
from api.views.core import BaseAPIView
from django.http import JsonResponse


class RetrieveRecordView(BaseAPIView):

    def get(self, request, id: int):
        record = models.GameRecord.objects.filter(id=id).first()

        if record is None:
            return JsonResponse({"detail": "not found"}, status=404)

        record_json = {
            "created": record.created.timestamp(),
            "game_mode": record.game_mode,
            "character_name": record.character_name,
            "tile": record.tile,
            "score": record.score,
            "turns": record.turns,
            "owner": record.owner.username
        }

        return JsonResponse(record_json)
