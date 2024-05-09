from api import models
from api.views.core import BaseAPIView
from api.models import JournalAccomplishment
from django.http import JsonResponse


class ListJournalAccomplishmentsView(BaseAPIView):
    MAX_RETURNED: int = 500

    def get(self, request):
        if (game_record_id := request.GET.get("id", None)) is None:
            return JsonResponse({"detail": "record id not specified"}, status=422)

        try:
            start = int(request.GET.get("start"))
            end = int(request.GET.get("end"))
        except (TypeError, ValueError):
            return JsonResponse({"detail": "start or end not specified"}, status=422)

        if end - start > self.MAX_RETURNED:
            return JsonResponse(
                {
                    "detail": f"cannot request more than {self.MAX_RETURNED} journal entries at once"
                },
                status=422,
            )

        record = models.GameRecord.objects.filter(id=game_record_id).first()
        if record is None:
            return JsonResponse(
                {"detail": f"record {game_record_id} not found"},
                status=404,
            )

        entries = JournalAccomplishment.objects.filter(game_record=record)[start:end]
        entries = [
            {"time": e.time, "text": e.text, "snapshot": e.snapshot} for e in entries
        ]

        return JsonResponse({"entries": entries}, status=200)
