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
