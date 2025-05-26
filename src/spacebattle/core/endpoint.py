from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/api/games/messages", methods=["POST"])
def receive_messages():
    data = request.get_json()
    print(data)
    return jsonify({"good": 1}), 200


if __name__ == "__main__":
    app.run(debug=True)
