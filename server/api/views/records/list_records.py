from django.http import JsonResponse
from api.views.core import BaseAPIView
from api import models


class ListRecordsView(BaseAPIView):
    def get(self, request, *args, **kwargs):
        records = models.GameRecord.objects.order_by("-created")[:10]

        record_list = []
        for r in records:
            r_dict = {
                "id": r.id,
                "created": r.created.timestamp(),
                "game_mode": r.game_mode,
                "character_name": r.character_name,
                "tile": r.tile,
                "score": r.score,
                "turns": r.turns,
            }
            record_list.append(r_dict)

        return JsonResponse({"records": record_list})
