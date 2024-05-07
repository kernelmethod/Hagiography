from api.views.core import BaseAPIView, TokenRequiredMixin
from django.http import JsonResponse


class CheckAPIKeyView(TokenRequiredMixin, BaseAPIView):
    required_scopes = ["upload"]

    def get(self, request):
        return JsonResponse({"detail": "token validated"})
