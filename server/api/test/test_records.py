import json

from api import schemas, models, utils
from api.test.utils import BaseTestCase, ApiClientTestCase
from datetime import datetime, timedelta, timezone
from django.test import Client


class JournalModelsTestCase(BaseTestCase):

    def test_parse_tile_collection(self):
        collection = "Tiles/tile-dirt1.png;.;&w;k;;0;0|Tiles/tile-dirt1.png;.;&w;k;;0;0|Tiles/tile-dirt1.png;';&w;k;;0;0|Terrain/sw_ground_dots1.png;ú;&w;w;;0;0|Terrain/sw_ground_dots3.png;ú;&w;w;;0;0|Terrain/sw_ground_dots3.png;ú;&w;w;;0;0|Terrain/sw_ground_dots3.png;ú;&w;w;;0;0|Tiles/tile-dirt1.png;.;&y;k;;0;0|Tiles/tile-dirt1.png;`;&y;k;;0;0|Terrain/sw_ground_dots2.png;ú;&w;w;;0;0|Tiles/tile-dirt1.png;';&w;k;;0;0|Tiles/tile-dirt1.png;.;&w;k;;0;0|Terrain/sw_ground_dots3.png;ú;&w;w;;0;0|Terrain/sw_ground_dots3.png;ú;&w;w;;0;0|Terrain/sw_ground_dots1.png;ú;&w;w;;0;0|Terrain/sw_ground_dots1.png;ú;&w;w;;0;0|tiles/sw_torch_nofire.png;ù;&r;w;;0;0|assets_content_textures_tiles_tile-grass1.png;.;&g;k;;0;0|Terrain/sw_ground_dots1.png;ú;&w;w;;0;0|Terrain/sw_ground_dots3.png;ú;&w;w;;0;0|Terrain/sw_ground_dots3.png;ú;&w;w;;0;0|Terrain/sw_ground_dots3.png;ú;&w;w;;0;0|creatures/caste_17.bmp;@;&Y;r;;0;0|Terrain/sw_ground_dots4.png;ú;&w;w;;0;0|Terrain/sw_ground_dots4.png;ú;&w;w;;0;0|assets_content_textures_tiles_tile-grass1.png;.;&G;k;;0;0|Terrain/sw_grass1.bmp;.;&G;k;;0;0|Tiles/tile-dirt1.png;,;&w;k;;0;0|Tiles/tile-dirt1.png;,;&w;k;;0;0|Terrain/sw_ground_dots4.png;ú;&w;w;;0;0|Terrain/sw_ground_dots4.png;ú;&w;w;;0;0|Terrain/sw_ground_dots2.png;ú;&w;w;;0;0|Terrain/sw_ground_dots3.png;ú;&w;w;;0;0|Terrain/sw_grass1.bmp;.;&g;k;;0;0|Tiles/tile-dirt1.png;,;&w;k;;0;0|Tiles/tile-dirt1.png;.;&y;k;;0;0|assets_content_textures_tiles_tile-grass1.png;`;&g;k;;0;0|Tiles/tile-dirt1.png;,;&w;k;;0;0|Terrain/sw_ground_dots1.png;ú;&w;w;;0;0|Terrain/sw_ground_dots1.png;ú;&w;w;;0;0|Terrain/sw_ground_dots2.png;ú;&w;w;;0;0|Terrain/sw_ground_dots1.png;ú;&w;w;;0;0|Terrain/sw_grass3.bmp;';&G;k;;0;0|assets_content_textures_tiles_tile-grass1.png;,;&g;k;;0;0|Tiles/tile-dirt1.png;';&w;k;;0;0"  # noqa: E501

        collection = utils.TileCollection.from_string(collection)
        self.assertEqual(len(collection), 9 * 5)


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

        self.character_tile = utils.Tile(
            path="Creatures/sw_trash_monk.bmp",
            render_string="",
            color_string="y",
            detail_color="r",
        )

        self.game_record = schemas.GameRecordCreate(
            game_mode="Crungle Mode",
            character_name="Sixshrew",
            tile=str(self.character_tile),
            score=12345,
            turns=67890,
        )

    def test_create_record(self):
        self.assertEqual(models.GameRecord.objects.count(), 1)
        response = self.client.put(
            self.endpoint,
            content_type="application/json",
            headers={"X-Access-Token": self.apitoken},
            data=self.game_record.model_dump_json(),
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(models.GameRecord.objects.count(), 2)

        id = response.json()["id"]
        record = models.GameRecord.objects.filter(id=id).first()
        self.assertEqual(record.game_mode, self.game_record.game_mode)
        self.assertEqual(record.character_name, self.game_record.character_name)
        self.assertEqual(str(record.tile), self.game_record.tile)
        self.assertEqual(record.score, self.game_record.score)
        self.assertEqual(record.turns, self.game_record.turns)
        self.assertEqual(record.build_code, self.game_record.build_code)

    def test_create_record_preauth(self):
        # Unauthenticated users, and users with invalid access tokens,
        # should not be able to create records.
        client = Client(enforce_csrf_checks=True)
        response = client.put(
            self.endpoint,
            content_type="application/json",
            data=self.game_record.model_dump_json(),
        )
        self.assertEqual(response.status_code, 401)


class RetrieveRecordTestCase(BaseTestCase):

    endpoint = "/api/records/id"

    def test_retrieve_record(self):
        record = models.GameRecord.objects.first()
        response = self.client.get(f"{self.endpoint}/{record.id}")
        self.assertEqual(response.status_code, 200)
        response = response.json()
        self.assertEqual(response.pop("game_mode"), record.game_mode)
        self.assertEqual(response.pop("character_name"), record.character_name)
        self.assertEqual(response.pop("tile"), str(record.tile))
        self.assertEqual(response.pop("score"), record.score)
        self.assertEqual(response.pop("turns"), record.turns)
        self.assertEqual(response.pop("owner"), record.owner.username)
        self.assertEqual(response.pop("build_code"), record.build_code)
        created = datetime.fromtimestamp(response.pop("created"), tz=timezone.utc)
        now = datetime.now(timezone.utc)
        self.assertTrue(now - created < timedelta(seconds=10))
        self.assertEqual(response, {})

    def test_retrieve_nonexistent_record(self):
        response = self.client.get(f"{self.endpoint}/beep_beep_boop")
        self.assertEqual(response.status_code, 404)


class UploadJournalEntriesTestCase(ApiClientTestCase):

    endpoint = "/api/records/journal/create"

    def setUp(self):
        super().setUp()
        self.record = models.GameRecord.objects.first()

        tiles = utils.TileCollection(tiles=[self.example_tile] * 5 * 9)
        journal_entry = schemas.JournalAccomplishmentCreate(
            text="On the 1st of Ut yara Ux, you arrived in Joppa.",
            time=1,
            snapshot=str(tiles),
        )
        self.body = schemas.JournalAccomplishmentsCreate(
            game_record_id=self.record.id, accomplishments=[journal_entry]
        )

    def test_create_journal_entries(self):
        original_num_entries = models.JournalAccomplishment.objects.count()
        response = self.client.put(
            self.endpoint,
            content_type="application/json",
            headers={"X-Access-Token": self.apitoken},
            data=self.body.model_dump_json(),
        )
        self.assertEqual(response.status_code, 200)

        # Check that the journal entries were added to the database
        current_num_entries = models.JournalAccomplishment.objects.count()
        self.assertEqual(current_num_entries, original_num_entries + 1)

    def test_create_with_bad_input(self):
        body = json.loads(self.body.model_dump_json())
        body.pop("game_record_id")
        response = self.client.put(
            self.endpoint,
            content_type="application/json",
            headers={"X-Access-Token": self.apitoken},
            data=json.dumps(body)
        )
        self.assertEqual(response.status_code, 422)

    def test_create_journal_entries_preauth(self):
        client = Client(enforce_csrf_checks=True)
        response = client.put(
            self.endpoint,
            content_type="application/json",
            data=self.body.model_dump_json(),
        )
        self.assertEqual(response.status_code, 401)

    def test_create_journal_entries_unauthorized(self):
        # Creating journal entries for a record that you don't own should result
        # in a 403 error.

        # Sign in as another user and generate an API key for them
        client = Client(enforce_csrf_checs=True)
        response = client.post(
            "/api/auth/login",
            content_type="application/json",
            data={"email": "user2@example.org", "password": "swordphish2"},
        )
        self.assertEqual(response.status_code, 200)

        response = client.post(
            "/api/auth/apikeys/generate",
            headers={"X-CSRFToken": client.cookies["csrftoken"].value},
        )
        self.assertEqual(response.status_code, 200)

        token = response.json()["token"]
        response = client.put(
            self.endpoint,
            content_type="application/json",
            headers={"X-Access-Token": token},
            data=self.body.model_dump_json(),
        )
        self.assertEqual(response.status_code, 403)

    def test_create_too_many_journal_entries(self):
        # Creating a very large number of journal entries should also result in
        # an error
        self.body.accomplishments *= 5001
        response = self.client.put(
            self.endpoint,
            content_type="application/json",
            headers={"X-Access-Token": self.apitoken},
            data=self.body.model_dump_json(),
        )
        self.assertEqual(response.status_code, 400)


class ListJournalEntriesTestCase(BaseTestCase):

    endpoint = "/api/records/journal/list"

    def setUp(self):
        super().setUp()
        self.record = models.GameRecord.objects.first()

    def test_list_records(self):
        endpoint = f"{self.endpoint}?id={self.record.id}&start=0&end=10"
        response = self.client.get(endpoint)
        self.assertEqual(response.status_code, 200)
        response = response.json()
        entries = response.pop("entries")
        self.assertEqual(response, {})
        self.assertEqual(len(entries), 1)
        entry = entries[0]
        self.assertEqual(entry.pop("time"), 101)
        self.assertEqual(entry.pop("text"), "On the 5th of Ut yara Ux, you abandoned all hope.")
        self.assertTrue(entry.pop("snapshot", None) is not None)
        self.assertEqual(entry, {})

    def test_retrieve_too_many_records(self):
        # Request more journal entries than allowed by the endpoint
        endpoint = f"{self.endpoint}?id={self.record.id}&start=0&end=501"
        response = self.client.get(endpoint)
        self.assertEqual(response.status_code, 422)

    def test_invalid_parameters(self):
        # id, start, and end parameters must all be specified
        endpoint = f"{self.endpoint}?id={self.record.id}&start=0"
        self.assertEqual(self.client.get(endpoint).status_code, 422)

        endpoint = f"{self.endpoint}?id={self.record.id}&end=10"
        self.assertEqual(self.client.get(endpoint).status_code, 422)

        endpoint = f"{self.endpoint}?start=0&end=10"
        self.assertEqual(self.client.get(endpoint).status_code, 422)

        # Try retrieving journal entries for a record that doesn't exist
        endpoint = f"{self.endpoint}?id=foo_bar_baz&start=0&end=10"
        self.assertEqual(self.client.get(endpoint).status_code, 404)
