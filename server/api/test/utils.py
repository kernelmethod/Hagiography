from api.models import GameRecord, User
from api.utils import Tile
from django.test import Client, TestCase


class BaseTestCase(TestCase):
    example_tile = Tile(
        path="Creatures/sw_trash_monk.bmp",
        render_string="",
        color_string="y",
        detail_color="r",
    )

    def populate():
        # Create a new user
        user = User(email="user@example.org", username="user")
        user.set_password("swordphish")
        user.save()

        user2 = User(email="user2@example.org", username="user2")
        user2.set_password("swordphish2")
        user2.save()

        # Pre-populate database
        GameRecord(
            game_mode="Classic",
            character_name="{{c|Resheph}}",
            tile=str(BaseTestCase.example_tile),
            score=12345,
            turns=67890,
            owner=user,
        ).save()

    def setUp(self):
        BaseTestCase.populate()
        self.client = Client(enforce_csrf_checks=True)
        self.test_user = User.objects.filter(username="user").first()


class AuthenticatedTestCase(BaseTestCase):
    """Test case variant where the client is now signed in to the
    server."""

    def setUp(self):
        super().setUp()
        response = self.client.post(
            "/api/auth/login",
            content_type="application/json",
            data={"email": "user@example.org", "password": "swordphish"},
        )
        self.assertEqual(response.status_code, 200)

        self.csrftoken = self.client.cookies["csrftoken"].value
        self.client.headers = {
            "X-CSRFToken": self.csrftoken
        }


class ApiClientTestCase(AuthenticatedTestCase):
    """Test case variant where the client has been supplied with an
    API token."""

    def setUp(self):
        super().setUp()
        response = self.client.post(
            "/api/auth/apikeys/generate",
            headers={"X-CSRFToken": self.csrftoken}
        )

        self.apitoken = response.json()["token"]
        self.client = Client(enforce_csrf_checks=True)
        self.client.headers = {
            "X-Access-Token": self.apitoken
        }
