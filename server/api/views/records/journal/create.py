from api import schemas
from api.models import GameRecord, JournalAccomplishment
from api.views.core import BaseAPIView, ExpectsJSONMixin, TokenRequiredMixin
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


class CreateJournalAccomplishmentsView(
    TokenRequiredMixin, ExpectsJSONMixin, BaseAPIView
):
    MAX_ACCOMPLISHMENTS: int = 5000

    required_scopes = ["upload"]
    input_model = schemas.JournalAccomplishmentsCreate

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def put(self, request):
        record = GameRecord.objects.filter(id=request.json.game_record_id).first()
        if record is None:
            return JsonResponse(
                {"detail": f"record {request.json.game_record_id} not found"},
                status=404,
            )

        if request.user.id != record.owner.id:
            return JsonResponse(
                {"detail": "you do not have permission to modify this record"},
                status=403,
            )

        accomplishments = request.json.accomplishments
        existing = record.journalaccomplishment_set.count()
        if existing + len(accomplishments) > self.MAX_ACCOMPLISHMENTS:
            return JsonResponse(
                {
                    "detail": "journal upload would exceed the maximum amount of journal entries for a single game record"
                },
                status=422,
            )

        acc = [
            JournalAccomplishment(game_record=record, time=j.time, snapshot=j.snapshot)
            for j in accomplishments
        ]
        JournalAccomplishment.objects.bulk_create(acc)

        return JsonResponse({"detail": "journal entries added successfully"})
