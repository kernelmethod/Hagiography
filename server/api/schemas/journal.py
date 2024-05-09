from api.utils import TileCollection
from pydantic import BaseModel


class JournalAccomplishment(BaseModel):

    time: int
    text: str
    snapshot: TileCollection


class JournalAccomplishmentsCreate(BaseModel):

    game_record_id: str
    accomplishments: list[JournalAccomplishment]


class JournalAccomplishmentsList(BaseModel):

    entries: list[JournalAccomplishment]
