from api import models
from api.schemas import GameRecordRetrieve
from api.views.core import BaseAPIView
from django.http import JsonResponse


class RetrieveRecordView(BaseAPIView):

    def get(self, request, id: int):
        record = models.GameRecord.objects.filter(id=id).first()

        if record is None:
            return JsonResponse({"detail": "not found"}, status=404)

        record_schema = GameRecordRetrieve(
            created=record.created.timestamp(),
            game_mode=record.game_mode,
            character_name=record.character_name,
            tile=str(record.tile),
            score=record.score,
            turns=record.turns,
            owner=record.owner.username,
            build_code=record.build_code
        )

        return JsonResponse(dict(record_schema))
