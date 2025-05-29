import json

from flask import Flask, jsonify, request

from src.spacebattle.commands.interpret import InterpretCommand
from src.spacebattle.core.message import Message

app = Flask(__name__)


@app.route("/api/games/messages", methods=["POST"])
def receive_messages():
    data = json.loads(request.get_json())
    message = Message(**data)
    print(f"ID игры {message.game_id}")
    print(f"ID объекта {message.object_id}")
    print(f"ID операции {message.operation_id}")
    print(f"Аргументы {message.args}")
    interpret_command = InterpretCommand(**message.model_dump())
    interpret_command.execute()
    # queue = IoC.resolve()
    return jsonify({}), 200


if __name__ == "__main__":
    app.run(debug=True)
