import json

from flask import Flask, jsonify, request

from src.spacebattle.commands.interpret import InterpretCommand
from src.spacebattle.core.message import Message

app = Flask(__name__)


@app.route("/api/games/messages", methods=["POST"])
def receive_messages():
    data = json.loads(request.get_json())
    message = Message(**data)
    interpret_command = InterpretCommand(**message.model_dump())
    interpret_command.execute()
    return jsonify({}), 200


if __name__ == "__main__":
    app.run(debug=True)
