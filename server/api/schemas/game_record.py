from pydantic import BaseModel


class BaseFullGameRecord(BaseModel):
    game_mode: str
    character_name: str
    tile: str
    score: int
    turns: int

    build_code: str | None = None


class GameRecordCreate(BaseFullGameRecord):
    pass


class GameRecordRetrieve(BaseFullGameRecord):
    created: float
    owner: str
