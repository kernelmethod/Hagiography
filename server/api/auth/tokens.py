from __future__ import annotations
import pyseto
import msgpack
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

    def serialize(self) -> bytes:
        return msgpack.packb([self.user_id, self.epoch, self.scopes])

    @classmethod
    def deserialize(cls, input: bytes) -> TokenPayload:
        user_id, epoch, scopes = msgpack.unpackb(input, use_list=False, raw=False)
        return cls(user_id=user_id, epoch=epoch, scopes=scopes)


class TokenFooter(BaseModel):
    expires: datetime

    def serialize(self) -> bytes:
        return msgpack.packb([self.expires.timestamp()])

    @classmethod
    def deserialize(cls, input: bytes) -> TokenFooter:
        (ts,) = msgpack.unpackb(input, use_list=False, raw=False)
        expires = datetime.fromtimestamp(ts, tz=timezone.utc)
        return cls(expires=expires)


class TokenFactory:

    KNOWN_SCOPES: set[str] = {"upload", "test__user", "test__admin"}

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

        if any(filter(lambda s: s not in self.KNOWN_SCOPES, payload.scopes)):
            raise ValueError(f"unknown scopes in {payload.scopes}")

        if footer is None:
            footer = TokenFooter(expires=datetime.now(timezone.utc) + expires_delta)
        elif expires_delta is not None:
            footer.expires = datetime.now(timezone.utc) + expires_delta

        payload_json = payload.serialize()
        footer_json = footer.serialize()

        token = pyseto.encode(self.key, payload=payload_json, footer=footer_json)

        return token.decode()

    def validate_token(self, token: str, scopes: list[str] | None = None) -> User:
        try:
            decoded = pyseto.decode(self.key, token)
        except ValueError:
            raise TokenValidationError("invalid token")

        footer = TokenFooter.deserialize(decoded.footer)

        if datetime.now(timezone.utc) > footer.expires:
            raise TokenValidationError("expired token")

        payload = TokenPayload.deserialize(decoded.payload)
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
