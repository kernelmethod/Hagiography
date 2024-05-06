import json
from django.http import JsonResponse
from django.views import View


class BaseAPIView(View):
    ...


class ExpectsJSONMixin:

    def dispatch(self, request, *args, **kwargs):
        if request.content_type != "application/json":
            return JsonResponse({"detail": "expected JSON"}, status=422)

        try:
            request.json = json.loads(request.body.decode())
        except Exception as _ex:    # noqa: F841
            return JsonResponse({"detail": "invalid body"}, status=422)

        return super().dispatch(request, *args, **kwargs)
