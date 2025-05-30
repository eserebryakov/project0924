from pydantic import BaseModel


class Message(BaseModel):
    game_id: str
    object_id: str
    operation_id: str
    args: object
