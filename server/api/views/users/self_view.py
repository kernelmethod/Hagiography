from api.views.core import BaseAPIView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse


class SelfView(LoginRequiredMixin, BaseAPIView):
    raise_exception = True

    def get(self, request):
        return JsonResponse(
            {"username": request.user.username, "email": request.user.email}
        )
