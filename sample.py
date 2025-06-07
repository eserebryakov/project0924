from uuid import uuid4

from requests import Session

session = Session()

user_id_1, user_id_2, user_id_3 = str(uuid4()), str(uuid4()), str(uuid4())
user_id_4 = str(uuid4())


response = session.post(
    url="http://127.0.0.1:5000/api/games/start", json={"participants": [user_id_1, user_id_2, user_id_3]}
)
game_id = response.json()["game_id"]

response = session.post(url="http://127.0.0.1:5000/api/auth/token", json={"game_id": game_id, "user_id": user_id_1})
print(game_id)
print(response.status_code)
print(response.json())
# ----------------------------------------------------------
response = session.post(url="http://127.0.0.1:5000/api/games/start", json={"participants": [user_id_4]})
game_id = response.json()["game_id"]

response = session.post(url="http://127.0.0.1:5000/api/auth/token", json={"game_id": game_id, "user_id": user_id_4})
print(game_id)
print(response.status_code)
print(response.json())
