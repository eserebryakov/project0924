from flask import Flask, request

app = Flask(__name__)


@app.route("/api/games/messages", methods=["POST"])
def receive_messages():
    data = request.get_json()
    print(data)


if __name__ == "__main__":
    app.run(debug=True)
