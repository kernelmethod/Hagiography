from api.utils import LazyTile, Tile
from django.db import models
from django.utils.translation import gettext_lazy as _


class TileField(models.CharField):

    description = _("Stringified tile specification")

    def __init__(self, *args, **kwargs) -> None:
        kwargs["max_length"] = 96
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs["max_length"]
        return name, path, args, kwargs

    def from_db_value(self, value, expression, connection) -> LazyTile | None:
        if value is None:
            return value
        return LazyTile.from_string(value)

    def to_python(self, value) -> LazyTile | None:
        if isinstance(value, (LazyTile, None)):
            return value
        return LazyTile(_tile=value)

    def get_prep_value(self, value: Tile | LazyTile) -> str:
        return str(value)
