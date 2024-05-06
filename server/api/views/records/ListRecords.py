from django.http import JsonResponse
from django.views import View
from api import models  # noqa: F401


class ListRecords(View):
    async def get(self, request, *args, **kwargs):
        return JsonResponse({"detail": "hello, world!"})
