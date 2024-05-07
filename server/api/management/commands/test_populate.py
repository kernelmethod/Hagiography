from api.test.utils import BaseTestCase
from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Populate the database with test data."

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        assert settings.DEBUG, "Cannot populate test database outside of DEBUG mode"
        BaseTestCase.populate()
