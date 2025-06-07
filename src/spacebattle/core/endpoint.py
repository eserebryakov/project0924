import json
import time
from concurrent.futures import ThreadPoolExecutor
from uuid import uuid4

from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, get_jwt, jwt_required
from requests import session

from src.spacebattle.commands.init import InitCommand
from src.spacebattle.commands.interpret import InterpretCommand
from src.spacebattle.commands.start_command import StartCommand
from src.spacebattle.common import constants
from src.spacebattle.core.message import Message
from src.spacebattle.scopes.ioc import IoC

app = Flask(__name__)
app.config[constants.JWT_SECRET_KEY] = constants.SECRET_KEY
app.config[constants.JWT_TOKEN_LOCATION] = [constants.HEADERS]
app.config[constants.JWT_HEADER_NAME] = constants.AUTHORIZATION
app.config[constants.JWT_HEADER_TYPE] = constants.BEARER
jwt = JWTManager(app)
executor = ThreadPoolExecutor()


@app.route("/api/games/start", methods=["POST"])
def start_game():
    game_id = uuid4()
    InitCommand().execute()
    start_command = StartCommand(game_id=game_id)
    start_command.execute()
    return jsonify({"game_id": game_id}), 200


@app.route("/api/games/start_sec", methods=["POST"])
def start_game_sec():
    response = session().post(url="http://127.0.0.1:5001/api/games/start", json=request.get_json())
    game_id = response.json()["game_id"]
    InitCommand().execute()
    start_command = StartCommand(game_id=game_id)
    start_command.execute()
    return jsonify({"game_id": game_id}), 200


@app.route("/api/games/messages", methods=["POST"])
def receive_messages():
    data = json.loads(request.get_json())
    message = Message(**data)
    interpret_command = InterpretCommand(**message.model_dump())
    queue_ = IoC.resolve(f"{constants.IOC_QUEUE}.{message.game_id}")
    queue_.put(interpret_command)
    time.sleep(0.1)
    obj_ = IoC.resolve(constants.GAME_OBJECT, message.game_id, message.object_id)
    message.args = obj_
    return jsonify(message.model_dump()), 200


@app.route("/api/games/messages_sec", methods=["POST"])
@jwt_required()
def receive_messages_sec():
    claims = get_jwt()
    user_game_id = claims["game_id"]

    data = json.loads(request.get_json())
    message = Message(**data)

    if message.game_id != user_game_id:
        return jsonify({"error": "Game ID mismatch"}), 403

    interpret_command = InterpretCommand(**message.model_dump())
    queue_ = IoC.resolve(f"{constants.IOC_QUEUE}.{message.game_id}")
    queue_.put(interpret_command)
    time.sleep(0.1)
    obj_ = IoC.resolve(constants.GAME_OBJECT, message.game_id, message.object_id)
    message.args = obj_
    return jsonify(message.model_dump()), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)
