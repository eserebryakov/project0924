from uuid import uuid4

from requests import Session

from src.spacebattle.common import constants
from src.spacebattle.common.vector import Vector
from src.spacebattle.core.message import Message

OBJECTS = [
    {
        "object_id": str(uuid4()),
        "location": Vector(2, 2).model_dump(),
        "velocity": Vector(0, 0).model_dump(),
    }
]

session = Session()
response = session.post(url="http://127.0.0.1:5000/api/games/start")
game_id = response.json()["game_id"]
object_id = OBJECTS[0]["object_id"]

message = Message(
    game_id=game_id,
    object_id=object_id,
    operation_id=constants.OPERATION_CREATE_OBJECT,
    args=OBJECTS[0],
)

response = session.post(
    url="http://127.0.0.1:5000/api/games/messages",
    json=message.model_dump_json(),
)
