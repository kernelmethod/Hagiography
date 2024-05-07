from api.views.core import BaseAPIView, ExpectsJSONMixin
from django.contrib.auth import authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.decorators.csrf import requires_csrf_token
from django.utils.decorators import method_decorator


class ChangePasswordView(LoginRequiredMixin, ExpectsJSONMixin, BaseAPIView):
    raise_exception = True

    @method_decorator(requires_csrf_token)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        password = request.json.get("password", None)
        if password is None:
            return JsonResponse({"detail": "old password not supplied"}, status=422)

        new_password = request.json.get("new_password", None)
        if new_password is None:
            return JsonResponse({"detail": "new password not supplied"}, status=422)

        if (user := authenticate(email=request.user, password=password)) is None:
            return JsonResponse({"detail": "the old password was invalid"}, status=401)

        user.set_password(new_password)
        user.save()
        return JsonResponse({"detail": "updated password"})
