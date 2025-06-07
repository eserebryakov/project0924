from typing import List

from pydantic import BaseModel

from src.spacebattle.core.user import User


class Game(BaseModel):
    participants: List[User]


class GamesDB(BaseModel):
    game_id: str
    participants: List[User]
