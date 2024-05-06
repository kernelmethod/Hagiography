from api.views.core import BaseAPIView, ExpectsJSONMixin
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie


class LoginView(ExpectsJSONMixin, BaseAPIView):

    @method_decorator(ensure_csrf_cookie)
    def post(self, request):
        email = request.json.get("email", None)
        password = request.json.get("password", None)

        if email is None or password is None:
            return JsonResponse(
                {"detail": "email or password not supplied"}, status=422
            )

        user = authenticate(request, email=email, password=password)
        if user is None:
            return JsonResponse(
                {"detail": "The email or password was invalid"}, status=401
            )

        login(request, user)
        return JsonResponse(
            {"detail": "The username or password was invalid"}, status=200
        )
