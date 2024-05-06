from api.test.utils import BaseTestCase


class SelfViewTestCase(BaseTestCase):

    def test_check_self_preauth(self):
        response = self.client.get("/api/users/self")
        self.assertEqual(response.status_code, 403)

    def test_check_self(self):
        response = self.client.post(
            "/api/auth/login",
            content_type="application/json",
            data={"email": "user@example.org", "password": "swordphish"}
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.get("/api/users/self")
        self.assertEqual(response.status_code, 200)
        response = response.json()
        self.assertEqual(response.pop("email"), "user@example.org")
        self.assertEqual(response.pop("username"), "user")
