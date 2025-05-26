from dataclasses import dataclass


@dataclass
class Message:
    game_id: str
    object_id: str
    operation_id: str
    args: str
