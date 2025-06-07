import json
from concurrent.futures import ThreadPoolExecutor
from uuid import uuid4

from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, get_jwt, jwt_required

from src.spacebattle.commands.init import InitCommand
from src.spacebattle.commands.interpret import InterpretCommand
from src.spacebattle.commands.start_command import StartCommand
from src.spacebattle.common import constants
from src.spacebattle.core.message import Message
from src.spacebattle.scopes.ioc import IoC

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "secret-space-battle-key"
app.config["JWT_TOKEN_LOCATION"] = ["headers"]
app.config["JWT_HEADER_NAME"] = "Authorization"
app.config["JWT_HEADER_TYPE"] = "Bearer"
jwt = JWTManager(app)
executor = ThreadPoolExecutor()


@app.route("/api/games/start", methods=["POST"])
def start_game():
    game_id = uuid4()
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

    def process_message():
        queue_.put(interpret_command)
        return IoC.resolve(constants.GAME_OBJECT, message.game_id, message.object_id)

    future = executor.submit(process_message)
    result = future.result()
    message.args = result
    return jsonify(message.model_dump()), 200


@app.route("/api/games/messages_sec", methods=["POST"])
@jwt_required()
def receive_messages_sec():
    data = json.loads(request.get_json())
    claims = get_jwt()
    user_game_id = claims["game_id"]
    user_id = claims["user_id"]
    print(user_game_id, user_id)

    data = json.loads(request.get_json())
    message = Message(**data)

    if message.game_id != user_game_id:
        return jsonify({"error": "Game ID mismatch"}), 403

    return jsonify({}), 200


if __name__ == "__main__":
    app.run(debug=True, port=5001)
