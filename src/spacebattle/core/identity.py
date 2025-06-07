from uuid import uuid4

from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "secret-space-battle-key"
jwt = JWTManager(app)

games_db = {}


@app.route("/api/games/start", methods=["POST"])
def create_game():
    participants = request.json.get("participants", [])
    game_id = str(uuid4())
    games_db[game_id] = {
        "participants": participants,
    }
    return jsonify({"game_id": game_id}), 201


@app.route("/api/auth/token", methods=["POST"])
def get_token():
    request.get_json()
    game_id = request.json.get("game_id")
    user_id = request.json.get("user_id")
    if not game_id or not user_id:
        return jsonify({"error": "game_id and user_id required"}), 400

    print(games_db)
    game = games_db.get(game_id)
    if not game or user_id not in game["participants"]:
        return jsonify({"error": "Unauthorized access"}), 403
    token_payload = {"game_id": game_id, "user_id": user_id}
    access_token = create_access_token(identity=user_id, additional_claims=token_payload)
    return jsonify(access_token=access_token), 200


if __name__ == "__main__":
    app.run(debug=True, port=5001)
