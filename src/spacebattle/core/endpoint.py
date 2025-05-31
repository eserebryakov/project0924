import json
from concurrent.futures import ThreadPoolExecutor
from uuid import uuid4

from flask import Flask, jsonify, request

from src.spacebattle.commands.init import InitCommand
from src.spacebattle.commands.interpret import InterpretCommand
from src.spacebattle.commands.start_command import StartCommand
from src.spacebattle.common import constants
from src.spacebattle.core.message import Message
from src.spacebattle.scopes.ioc import IoC

app = Flask(__name__)
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


if __name__ == "__main__":
    app.run(debug=True)
