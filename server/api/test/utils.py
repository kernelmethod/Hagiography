from api.models import GameRecord, User
from api.utils import Tile
from django.test import Client, TestCase


class BaseTestCase(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)

        # Create a new user
        user = User(email="user@example.org", username="user")
        user.set_password("swordphish")
        user.save()

        # Pre-populate database
        tile = Tile(
            path="Creatures/sw_trash_monk.bmp",
            render_string="",
            color_string="y",
            detail_color="r",
        )

        GameRecord(
            game_mode="Classic",
            character_name="{{c|Resheph}}",
            tile=str(tile),
            score=12345,
            turns=67890,
        ).save()
