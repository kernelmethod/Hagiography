from api.utils import TileCollection
from pydantic import BaseModel


class JournalAccomplishment(BaseModel):

    time: int
    text: str
    snapshot: TileCollection


class JournalAccomplishmentCreate(BaseModel):

    time: int
    text: str
    snapshot: str


class JournalAccomplishmentsCreate(BaseModel):

    game_record_id: str
    accomplishments: list[JournalAccomplishmentCreate]


class JournalAccomplishmentsList(BaseModel):

    entries: list[JournalAccomplishment]
