from api.views.core import BaseAPIView
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse


class LogoutView(LoginRequiredMixin, BaseAPIView):
    raise_exception = True

    def post(self, request):
        logout(request)
        return JsonResponse({"detail": "logout successful"})
