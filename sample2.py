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

game_id = "41a98ea1-06c1-4c3e-9eaf-7cd2a3fc33b6"
object_id = TEST_OBJECT["object_id"]
message = Message(
    game_id=game_id,
    object_id=object_id,
    operation_id=constants.OPERATION_CREATE_OBJECT,
    args=TEST_OBJECT,
)

token_ = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0OTI5OTEyMSwianRpIjoiMjViZGNmZWEtYjZkNC00MzcwLTgzYmItZDFkOGJjNGRhYmM2IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjBlNjE2OWVhLTY0ZGItNGQ4Ny1iYTBkLWE0YjIzNDBiNzdiMyIsIm5iZiI6MTc0OTI5OTEyMSwiY3NyZiI6IjZmODFjMjk1LTllYmUtNDkxMC1iZTRjLTlmNWQxMjgzNjE0MCIsImV4cCI6MTc0OTMwMDAyMSwiZ2FtZV9pZCI6IjQxYTk4ZWExLTA2YzEtNGMzZS05ZWFmLTdjZDJhM2ZjMzNiNiIsInVzZXJfaWQiOiIwZTYxNjllYS02NGRiLTRkODctYmEwZC1hNGIyMzQwYjc3YjMifQ.Ae83geadOmAOKAtXAw9s9mNAsFO9XpQ_8vv2O9EFH_k"

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
