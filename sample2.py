from uuid import uuid4

from requests import Session

from src.spacebattle.common import constants
from src.spacebattle.common.vector import Vector
from src.spacebattle.core.message import Message

TEST_OBJECT = {
    "object_id": str(uuid4()),
    "location": Vector(2, 2).model_dump(),
    "velocity": Vector(0, 0).model_dump(),
}

game_id = "dd5ee501-fc37-4173-8559-9da02c3e82b2"
object_id = TEST_OBJECT["object_id"]
message = Message(
    game_id=game_id,
    object_id=object_id,
    operation_id=constants.OPERATION_CREATE_OBJECT,
    args=TEST_OBJECT,
)

token_ = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0OTI5ODY3NSwianRpIjoiNWQwMGE5NTYtODc1OS00MTViLWFlZWMtZDI2NmQyMjVjMDFhIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjllN2NkYzQxLWRkMDItNGRkNS04YzM3LTc4YjRjMzg2ZjI3NyIsIm5iZiI6MTc0OTI5ODY3NSwiY3NyZiI6ImY1MjRhZTZhLTI5NDctNGU3YS04NjkxLTE5YTI4MDU1MTE2ZiIsImV4cCI6MTc0OTI5OTU3NSwiZ2FtZV9pZCI6IjY1M2ZhN2YwLTZlY2QtNGVhNS05M2I4LWVjNDUxYjZkOTQwNiIsInVzZXJfaWQiOiI5ZTdjZGM0MS1kZDAyLTRkZDUtOGMzNy03OGI0YzM4NmYyNzcifQ.utrXQmZHSwoZgED_B1_dPLIPVEJFVM6TjOE7WapAAAQ"

session = Session()

response = session.post(
    url="http://127.0.0.1:5001/api/games/messages_sec",
    headers={
        "Authorization": "Bearer " + token_,
    },
    json=message.model_dump_json(),
)
print(response.status_code)
print(response.text)
print(response.json())
