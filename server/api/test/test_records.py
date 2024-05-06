from api.models import GameRecord
from api.utils import Tile
from datetime import datetime, timedelta, timezone
from django.test import AsyncClient, TestCase


class ListRecordsTestCase(TestCase):
    def setUp(self):
        self.client = AsyncClient()

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

    async def test_list_records(self):
        response = await self.client.get("/api/records/list")
        self.assertEqual(response.status_code, 200)
        records = response.json()["records"]
        self.assertEqual(len(records), 1)
        record = records[0]
        self.assertEqual(record.pop("game_mode"), "Classic")
        self.assertEqual(record.pop("character_name"), "{{c|Resheph}}")
        self.assertEqual(record.pop("score"), 12345)
        self.assertEqual(record.pop("turns"), 67890)
        self.assertTrue(record.pop("tile", None) is not None)
        self.assertTrue(record.pop("id", None) is not None)
        created = datetime.fromisoformat(record.pop("created"))
        now = datetime.now(timezone.utc)
        self.assertTrue(now - created < timedelta(seconds=10))
        self.assertEqual(record, dict())
