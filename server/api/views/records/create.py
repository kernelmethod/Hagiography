from api import schemas
from api.models import GameRecord
from api.views.core import BaseAPIView, ExpectsJSONMixin, TokenRequiredMixin
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


class CreateRecordView(TokenRequiredMixin, ExpectsJSONMixin, BaseAPIView):
    required_scopes = ["upload"]
    input_model = schemas.GameRecordCreate

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def put(self, request):
        record = GameRecord(
            game_mode=request.json.game_mode,
            character_name=request.json.character_name,
            tile=request.json.tile,
            score=request.json.score,
            turns=request.json.turns,
            owner=request.user,
        )
        record.save()
        return JsonResponse({"detail": "record created successfuly", "id": record.id})
