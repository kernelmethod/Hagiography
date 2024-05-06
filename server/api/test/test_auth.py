from api.test.utils import BaseTestCase


class LoginTestCase(BaseTestCase):

    def test_login(self):
        response = self.client.post(
            "/api/auth/login",
            content_type="application/json",
            data={"email": "user@example.org", "password": "swordphish"},
        )
        self.assertEqual(response.status_code, 200)

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


class ChangePasswordTestCase(BaseTestCase):

    endpoint = "/api/auth/change_password"

    def test_change_password_preauth(self):
        response = self.client.post(
            self.endpoint,
            content_type="application/json",
            data={"password": "swordphish", "new_password": "swordphish2"}
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
            data={"password": "swordphish"}
        )
        self.assertEqual(response.status_code, 422)

        response = self.client.post(
            self.endpoint,
            content_type="application/json",
            headers={"X-CSRFToken": token.value},
            data={"new_password": "swordphish"}
        )
        self.assertEqual(response.status_code, 422)

        # Check that the endpoint requires CSRF protection
        response = self.client.post(
            self.endpoint,
            content_type="application/json",
            data={"password": "swordphish2", "new_password": "swordphish3"},
        )
        self.assertEqual(response.status_code, 403)
