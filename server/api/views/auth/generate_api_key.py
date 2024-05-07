from api.auth import TokenFactory, TokenPayload
from api.views.core import BaseAPIView
from datetime import timedelta
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.decorators.csrf import requires_csrf_token
from django.utils.decorators import method_decorator


class GenerateAPIKeyView(LoginRequiredMixin, BaseAPIView):
    raise_exception = True

    @method_decorator(requires_csrf_token)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        factory = TokenFactory()
        expires_delta = timedelta(days=2**16)
        payload = TokenPayload(
            user_id=request.user.id,
            epoch=request.user.token_epoch,
            scopes=["upload"]
        )
        token = factory.create_token(payload, expires_delta=expires_delta)
        return JsonResponse({"token": token})
