from api.auth import TokenFactory
from api.test.utils import BaseTestCase, AuthenticatedTestCase
from django.test import Client


class LoginTestCase(BaseTestCase):

    def test_login(self):
        response = self.client.post(
            "/api/auth/login",
            content_type="application/json",
            data={"email": "user@example.org", "password": "swordphish"},
        )
        self.assertEqual(response.status_code, 200)
        json = response.json()
        self.assertEqual(json.pop("detail"), "login successful")
        self.assertEqual(json.pop("username"), self.test_user.username)
        self.assertEqual(json.pop("id"), self.test_user.id)
        self.assertEqual(json, {})

        # The login view should ensure that the user has CSRF cookies
        # set so that authorized API endpoints can be CSRF-protected.
        self.assertTrue("csrftoken" in response.cookies)

    def test_invalid_request(self):
        response = self.client.post("/api/auth/login")
        self.assertEqual(response.status_code, 422)
        response = self.client.post(
            "/api/auth/login",
            content_type="application/json",
            # Should be email, not username
            data={"username": "user@example.org", "password": "swordphish"},
        )
        self.assertEqual(response.status_code, 422)


class LogoutTestCase(AuthenticatedTestCase):

    endpoint = "/api/auth/logout"

    def test_logout(self):
        response = self.client.get("/api/users/self")
        self.assertEqual(response.status_code, 200)

        # Logout should require CSRF token
        response = self.client.post(self.endpoint)
        self.assertEqual(response.status_code, 403)

        response = self.client.post(
            self.endpoint, headers={"X-CSRFToken": self.csrftoken}
        )
        self.assertEqual(response.status_code, 200)

        # Now we should be unable to access the self endpoint
        response = self.client.get("/api/users/self")
        self.assertEqual(response.status_code, 403)


class ChangePasswordTestCase(BaseTestCase):

    endpoint = "/api/auth/change_password"

    def test_change_password_preauth(self):
        response = self.client.post(
            self.endpoint,
            content_type="application/json",
            data={"password": "swordphish", "new_password": "swordphish2"},
        )
        self.assertEqual(response.status_code, 403)

    def test_change_password(self):
        def login(password):
            response = self.client.post(
                "/api/auth/login",
                content_type="application/json",
                data={"email": "user@example.org", "password": password},
            )
            return response.status_code

        self.assertEqual(login("swordphish"), 200)
        token = self.client.cookies["csrftoken"]
        response = self.client.post(
            self.endpoint,
            content_type="application/json",
            headers={"X-CSRFToken": token.value},
            data={"password": "swordphish", "new_password": "swordphish2"},
        )
        self.assertEqual(response.status_code, 200)

        # Old password should now be invalid
        self.assertEqual(login("swordphish"), 401)
        self.assertEqual(login("swordphish2"), 200)

        # If we attempt to update the password again, we need to use the
        # new password.
        token = self.client.cookies["csrftoken"]
        response = self.client.post(
            self.endpoint,
            content_type="application/json",
            headers={"X-CSRFToken": token.value},
            data={"password": "swordphish", "new_password": "swordphish3"},
        )
        self.assertEqual(response.status_code, 401)

        # Check that we get errors if we submit invalid data
        token = self.client.cookies["csrftoken"]
        response = self.client.post(
            self.endpoint,
            content_type="application/json",
            headers={"X-CSRFToken": token.value},
            data={"password": "swordphish"},
        )
        self.assertEqual(response.status_code, 422)

        response = self.client.post(
            self.endpoint,
            content_type="application/json",
            headers={"X-CSRFToken": token.value},
            data={"new_password": "swordphish"},
        )
        self.assertEqual(response.status_code, 422)

        # Check that the endpoint requires CSRF protection
        response = self.client.post(
            self.endpoint,
            content_type="application/json",
            data={"password": "swordphish2", "new_password": "swordphish3"},
        )
        self.assertEqual(response.status_code, 403)


class GenerateAPIKeyTestCase(AuthenticatedTestCase):

    generate_endpoint = "/api/auth/apikeys/generate"
    check_endpoint = "/api/auth/apikeys/check"

    def test_generate_api_key(self):
        # Generate an API key, and then validate that it's correct
        response = self.client.post(
            self.generate_endpoint, headers={"X-CSRFToken": self.csrftoken}
        )
        self.assertTrue("token" in response.json())

        token = response.json()["token"]
        factory = TokenFactory()

        factory.validate_token(token, scopes=["upload"])

        # Check that the API key is correct. The check endpoint should initially
        # return an error
        client = Client(enforce_csrf_checks=True)
        response = client.get(self.check_endpoint)
        self.assertEqual(response.status_code, 401)

        response = client.get(self.check_endpoint, headers={"X-Access-Token": token})
        self.assertEqual(response.status_code, 200)
