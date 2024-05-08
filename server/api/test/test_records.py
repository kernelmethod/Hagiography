from api import schemas
from api.models import GameRecord
from api.test.utils import BaseTestCase, ApiClientTestCase
from api.utils import Tile
from datetime import datetime, timedelta, timezone
from django.test import Client


class ListRecordsTestCase(BaseTestCase):

    def test_list_records(self):
        response = self.client.get("/api/records/list")
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
        created = datetime.fromtimestamp(record.pop("created"), tz=timezone.utc)
        now = datetime.now(timezone.utc)
        self.assertTrue(now - created < timedelta(seconds=10))
        self.assertEqual(record, dict())


class CreateRecordTestCase(ApiClientTestCase):

    endpoint = "/api/records/create"

    def setUp(self):
        super().setUp()

        self.character_tile = Tile(
            path="Creatures/sw_trash_monk.bmp",
            render_string="",
            color_string="y",
            detail_color="r"
        )

        self.game_record = schemas.GameRecordCreate(
            game_mode="Crungle Mode",
            character_name="Sixshrew",
            tile=str(self.character_tile),
            score=12345,
            turns=67890
        )

    def test_create_record(self):
        self.assertEqual(GameRecord.objects.count(), 1)
        response = self.client.put(
            self.endpoint,
            content_type="application/json",
            headers={"X-Access-Token": self.apitoken},
            data=self.game_record.model_dump_json()
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(GameRecord.objects.count(), 2)

        id = response.json()["id"]
        record = GameRecord.objects.filter(id=id).first()
        self.assertEqual(record.game_mode, self.game_record.game_mode)
        self.assertEqual(record.character_name, self.game_record.character_name)
        self.assertEqual(record.tile, self.game_record.tile)
        self.assertEqual(record.score, self.game_record.score)
        self.assertEqual(record.turns, self.game_record.turns)

    def test_create_record_preauth(self):
        # Unauthenticated users, and users with invalid access tokens,
        # should not be able to create records.
        client = Client(enforce_csrf_checks=True)
        response = client.put(
            self.endpoint,
            content_type="application/json",
            data=self.game_record.model_dump_json()
        )
        self.assertEqual(response.status_code, 401)


class RetrieveRecordTestCase(BaseTestCase):

    endpoint = "/api/records/id"

    def test_retrieve_record(self):
        record = GameRecord.objects.first()
        response = self.client.get(f"{self.endpoint}/{record.id}")
        self.assertEqual(response.status_code, 200)
        response = response.json()
        self.assertEqual(response.pop("game_mode"), record.game_mode)
        self.assertEqual(response.pop("character_name"), record.character_name)
        self.assertEqual(response.pop("tile"), record.tile)
        self.assertEqual(response.pop("score"), record.score)
        self.assertEqual(response.pop("turns"), record.turns)
        self.assertEqual(response.pop("owner"), record.owner.username)
        created = datetime.fromtimestamp(response.pop("created"), tz=timezone.utc)
        now = datetime.now(timezone.utc)
        self.assertTrue(now - created < timedelta(seconds=10))
        self.assertEqual(response, {})

    def test_retrieve_nonexistent_record(self):
        response = self.client.get(f"{self.endpoint}/beep_beep_boop")
        self.assertEqual(response.status_code, 404)
