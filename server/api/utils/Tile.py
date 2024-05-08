from __future__ import annotations
from typing import Any
from pydantic import BaseModel, model_validator


class Tile(BaseModel):

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
        if len(components) != 7:
            raise ValueError("unable to parse string as tile spec")

        return cls(
            path=components[0],
            render_string=components[1],
            color_string=components[2],
            detail_color=components[3],
            tile_color=None if components[4] == "" else components[4],
            hflip=(components[5] == "1"),
            vflip=(components[6] == "1"),
        )

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


class TileCollection(BaseModel):
    tiles: list[Tile]

    @classmethod
    def from_string(self, s: str) -> TileCollection:
        tiles = [Tile(t) for t in s.split("|")]
        return TileCollection(tiles=tiles)

    def __str__(self) -> str:
        return "|".join(str(t) for t in self.tiles)


class LazyTile(BaseModel):
    # Lazily-parsed tile
    spec_: str | None = None
    tile_: Tile | None = None

    @model_validator(mode="after")
    def check_specified(self) -> LazyTile:
        if self.spec_ is None and self.tile_ is None:
            raise ValueError("one of spec_ or tile_ must be set")

    @classmethod
    def from_string(cls, s: str) -> LazyTile:
        return LazyTile(spec_=s)

    def __str__(self) -> str:
        return self.spec

    @property
    def tile(self) -> Tile:
        if self.tile_ is None:
            self.tile_ = Tile.from_string(self.spec)
        return self.tile_

    @property
    def spec(self) -> str:
        if self.spec_ is None:
            self.spec_ = str(self.tile_)
        return self.spec_

    @property
    def path(self) -> str:
        return self.tile.path

    @property
    def render_string(self) -> str:
        return self.tile.render_string

    @property
    def color_string(self) -> str:
        return self.tile.color_string

    @property
    def detail_color(self) -> str:
        return self.tile.detail_color

    @property
    def tile_color(self) -> str:
        return self.tile.tile_color

    @property
    def hflip(self) -> bool:
        return self.tile.hflip

    @property
    def vflip(self) -> bool:
        return self.tile.vflip


class LazyTileCollection(BaseModel):
    # Lazily-parsed tile collection
    spec_: str | None = None
    tiles_: Tile | None = None

    @model_validator(mode="after")
    def check_specified(self) -> LazyTile:
        if self.spec_ is None and self.tile_ is None:
            raise ValueError("one of spec_ or tile_ must be set")

    @classmethod
    def from_string(cls, s: str) -> LazyTile:
        return LazyTileCollection(spec_=s)

    def __str__(self) -> str:
        return self.spec

    @property
    def tiles(self) -> Tile:
        if self.tiles_ is None:
            self.tiles_ = TileCollection.from_string(self.spec)
        return self.tiles_

    @property
    def spec(self) -> str:
        if self.spec_ is None:
            self.spec_ = str(self.tiles_)
        return self.spec_
