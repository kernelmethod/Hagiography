from api import utils
from api.models import GameRecord, User, JournalAccomplishment
from api.utils import Tile
from django.test import Client, TestCase


class BaseTestCase(TestCase):
    example_tile = Tile(
        path="Creatures/sw_trash_monk.bmp",
        render_string="",
        color_string="y",
        detail_color="r",
    )

    example_build_code = """H4sIAAAAAAAAA81WW2vbMBR+L/Q/CLNHJyShdCOQhywda7cW0tp0g9EH2T7YWmXJ6LKShfz3HtlpYsdt03ZrSCAo0ncun84tmh8eEOKlNIc/oDSTwhsSb9DtdQe94+7go+eXeGQZT2oCfRToLbFcJpaDxuNfbk/IvFpWUDgrwCn9vDrvTjKqaGxAfXYWdffSJu77FYQ0KHZRKvhkrDXkEZ91JgEqFD65rnyP1sx8MrHcWAUjAdYoyn0ytRFn8XeYhfIWxEhYziuOJZmEGoo0Vuzw6IN5LbUTNNKit3aCNh/kndkLa6iBhJzanIqGVCuWD9ii+rHw3xzLwEZ7GsoGs+2RXIo7o2MVS0Gt2VUMy8Shbb2HUdzgtj2OeYEWe/UTDRzi0sa6a6vPvL4hywpeBvlE4nWgk1sdc0jqLkrRa6oYFQYl3T030Ym0Jdavny/8l/o+BZZmBgQ206Vl8a0ArXfMQCrxnMtKgARMpBxacv/oPFSswND/lkyYXYc+vJOdDKjaueMzpZihWHLEzdS8HdS3eF9vbp6cJf3/OkvGxigWWQP7OEw2yW2fJlNXg3pqVZxRjSUxbObQC4wCkZoMgU+NlHjjlHFmZm0glDbNyo4ekuMmdIb1zjlLQcTQVvzBOC/kHag29CWVztr6rF53Hi2CAsrq6BwdNYEryCkT2MWbQzPC647dKG1qvOO/0MRqI3P2F1b4HlbQUyS3V5LAR2e7d70CHuloDysgKfPcEldSYKcHj2q9Z3IyKTUEBgcjFsu5jMu5tY8JeoboCx5hG3rO2TdZFPR1TzG33Bwe4HoPft6vRHEMAAA="""     # noqa: E501

    def populate():
        # Create a new user
        user = User(email="user@example.org", username="user")
        user.set_password("swordphish")
        user.save()

        user2 = User(email="user2@example.org", username="user2")
        user2.set_password("swordphish2")
        user2.save()

        # Pre-populate database
        record = GameRecord(
            game_mode="Classic",
            character_name="{{c|Resheph}}",
            tile=str(BaseTestCase.example_tile),
            score=12345,
            turns=67890,
            owner=user,
            build_code=BaseTestCase.example_build_code,
        )
        record.save()

        tiles = utils.TileCollection(tiles=[BaseTestCase.example_tile] * 5 * 9)
        journal_entry = JournalAccomplishment(
            game_record=record,
            text="On the 5th of Ut yara Ux, you abandoned all hope.",
            time=101,
            snapshot=str(tiles),
        )
        journal_entry.save()

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
