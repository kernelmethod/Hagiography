from abc import ABC, abstractmethod
from api.auth import TokenFactory, TokenValidationError
from django.http import JsonResponse
from django.views import View
from pydantic import BaseModel
from pydantic_core import from_json
from typing import Type


class BaseAPIView(View):
    pass


class ExpectsJSONMixin:

    input_model: Type[BaseModel] | None = None

    def dispatch(self, request, *args, **kwargs):
        if request.content_type != "application/json":
            return JsonResponse({"detail": "expected JSON"}, status=422)

        try:
            json = from_json(request.body)
            if self.input_model is None:
                request.json = json
            else:
                request.json = self.input_model.model_validate(json)
        except Exception as _ex:  # noqa: F841
            return JsonResponse({"detail": "invalid body"}, status=422)

        return super().dispatch(request, *args, **kwargs)


class TokenRequiredMixin(ABC):

    @property
    @abstractmethod
    def required_scopes(self) -> list[str]:
        pass

    def dispatch(self, request, *args, **kwargs):
        if (token := request.headers.get("X-Access-Token", None)) is None:
            return JsonResponse({"detail": "missing token"}, status=401)

        factory = TokenFactory()

        try:
            request.user = factory.validate_token(token, scopes=self.required_scopes)
        except TokenValidationError:
            return JsonResponse({"detail": "invalid or expired token"}, status=401)

        return super().dispatch(request, *args, **kwargs)
