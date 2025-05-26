from requests import Session

from src.spacebattle.core.message import Message

message = Message(
    game_id="game1",
    object_id="object1",
    operation_id="operation1",
    args={"x": 5, "y": 5},
)

session = Session()

response = session.post(
    url="http://127.0.0.1:5000/api/games/messages",
    json=message.model_dump_json(),
)
print(response.status_code)
print(response.text)
print(response.json())
