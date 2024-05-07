from pydantic import BaseModel


class GameRecordCreate(BaseModel):
    game_mode: str
    character_name: str
    tile: str
    score: int
    turns: int
