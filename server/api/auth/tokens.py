import json
import pyseto
from api.models import User
from datetime import datetime, timedelta, timezone
from django.conf import settings
from pydantic import BaseModel, Field


class TokenValidationError(Exception):
    pass


class TokenPayload(BaseModel):
    user_id: int
    epoch: int
    scopes: list[str] = Field(default_factory=lambda: list())


class TokenFooter(BaseModel):
    expires: datetime


class TokenFactory:

    def __init__(self) -> None:
        self.key = pyseto.Key.new(version=4, purpose="local", key=settings.TOKEN_KEY)

    def create_token(
        self,
        payload: TokenPayload,
        footer: TokenFooter | None = None,
        expires_delta: timedelta | None = None,
    ) -> str:
        if footer is None and expires_delta is None:
            raise ValueError(
                "at least one of footer or expires_delta must be specified"
            )

        if footer is None:
            footer = TokenFooter(expires=datetime.now(timezone.utc) + expires_delta)
        elif expires_delta is not None:
            footer.expires = datetime.now(timezone.utc) + expires_delta

        payload_json = payload.model_dump_json().encode("utf-8")
        footer_json = footer.model_dump_json().encode("utf-8")

        token = pyseto.encode(self.key, payload=payload_json, footer=footer_json)

        return token.decode()

    def validate_token(self, token: str, scopes: list[str] | None = None) -> User:
        decoded = pyseto.decode(self.key, token)

        footer = TokenFooter(**json.loads(decoded.footer.decode()))

        if datetime.now(timezone.utc) > footer.expires:
            raise TokenValidationError("expired token")

        payload = TokenPayload(**json.loads(decoded.payload.decode()))
        if scopes is not None:
            if any(filter(lambda s: s not in payload.scopes, scopes)):
                raise TokenValidationError("insufficient permissions")

        # Validate that the epoch is not expired
        user = User.objects.filter(id=payload.user_id).first()
        if user is None:
            raise TokenValidationError("no user found with given ID")
        if payload.epoch < user.token_epoch:
            raise TokenValidationError("token epoch expired")

        return user
