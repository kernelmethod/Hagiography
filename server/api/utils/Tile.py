from __future__ import annotations
from dataclasses import dataclass
from typing import Any


@dataclass
class Tile:

    path: str
    render_string: str
    color_string: str
    detail_color: str
    tile_color: str | None = None

    hflip: bool = False
    vflip: bool = False

    @classmethod
    def from_string(cls, s: str) -> Tile:
        components: list[Any] = s.split(";")
        if len(s) != 7:
            raise ValueError("unable to parse string as tile spec")

        components[4] = None if components[4] == "" else components[4]
        components[5] = components[5] == "1"
        components[6] = components[6] == "1"

        return cls(*components)  # type: ignore

    def __str__(self):
        return ";".join(
            [
                self.path,
                self.render_string,
                self.color_string,
                self.detail_color,
                "" if self.tile_color is None else self.tile_color,
                str(int(self.hflip)),
                str(int(self.vflip)),
            ]
        )
