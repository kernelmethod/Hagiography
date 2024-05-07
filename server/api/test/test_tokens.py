# Tests for token issuance using TokenFactory

from api.auth import TokenFactory, TokenPayload, TokenValidationError
from api.models import User
from datetime import timedelta
from django.test import TestCase


class TokenFactoryTestCase(TestCase):
    def setUp(self):
        user = User(email="user@example.org", username="user", id=123)
        user.set_password("swordphish")
        user.save()

        self.default_payload = TokenPayload(user_id=user.id, epoch=user.token_epoch)
        self.default_expires_delta = timedelta(minutes=1)
        self.factory = TokenFactory()

    def test_create_token(self):
        token = self.factory.create_token(
            self.default_payload, expires_delta=self.default_expires_delta
        )

        self.assertTrue(isinstance(token, str))

        # Validate that we can decode the token correctly
        user = self.factory.validate_token(token)
        self.assertEqual(user.email, "user@example.org")

    def test_create_expired_token(self):
        # Tokens that are expired should raise an exception when we attempt
        # to decode them.
        token = self.factory.create_token(
            self.default_payload, expires_delta=timedelta(seconds=-5)
        )

        with self.assertRaises(Exception):
            self.factory.validate_token(token)

    def test_validate_token_with_scopes(self):
        payload = TokenPayload(user_id=123, epoch=456, scopes=["test__user"])
        token = self.factory.create_token(
            payload, expires_delta=self.default_expires_delta
        )

        # With no scopes and the user scope, the token should be correctly validated
        self.factory.validate_token(token)
        self.factory.validate_token(token, scopes=["test__user"])

        # With scopes that are not included in the token's scope, an exception
        # should be raised.
        with self.assertRaises(TokenValidationError):
            self.factory.validate_token(token, scopes=["test__admin"])

    def test_token_invalidation_after_password_change(self):
        token = self.factory.create_token(
            self.default_payload, expires_delta=self.default_expires_delta
        )

        self.assertTrue(isinstance(token, str))
        user = self.factory.validate_token(token)

        # Token should no longer be valid once the user's password is updated
        user.set_password("swordphish2")
        user.save()

        user = User.objects.filter(id=123).first()
        with self.assertRaises(TokenValidationError):
            self.factory.validate_token(token)
