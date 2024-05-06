from django.http import JsonResponse
from django.views import View
from api import models  # noqa: F401


class ListRecords(View):
    async def get(self, request, *args, **kwargs):
        records = models.GameRecord.objects.order_by("-created")[:10]

        record_list = []
        async for r in records:
            r_dict = {
                "id": r.id,
                "created": r.created,
                "game_mode": r.game_mode,
                "character_name": r.character_name,
                "tile": r.tile,
                "score": r.score,
                "turns": r.turns,
            }
            record_list.append(r_dict)

        return JsonResponse({"records": record_list})
