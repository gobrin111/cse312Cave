from flask import Blueprint, make_response, request
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from bson import ObjectId
import json
import html
import hashlib
import os
game_bp = Blueprint("game", __name__)

MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://mongo:27017/wurdle')
mongo_client = MongoClient(MONGO_URI)
db = mongo_client["wurdle"]
user_collection = db["users"]
chat_collection = db["chat"]
like_collection = db["like"]
# the active score collection keeps track of the scores that user currently have
active_score_collection = db["score"]
# when the scoreboard is being displayed, it will look this db to determine what to display
board_score_collection = db["board"]


@game_bp.route("/send_score", methods=["POST"])
def send_score():
    data = request.get_json()
    score = data["score"]
    response = make_response(json.dumps({"score": score}), 200)

    if "auth_token" in request.cookies:
        auth_token = request.cookies.get("auth_token")
        auth_token = hashlib.sha256(auth_token.encode('utf-8')).hexdigest()

        if user_collection.find_one({"auth_token": auth_token}):
            account = user_collection.find_one({"auth_token": auth_token})
            username = account.get("username")
            if active_score_collection.find_one({"username": username}):
                new_score = active_score_collection.find_one({"username": username})["score"] + score
                active_score_collection.update_one({"username": username}, {"$set": {"score": new_score}})
                response = make_response({"score": new_score}, 200)
            else:
                active_score_collection.insert_one({"username": username, "score": score})
    else:
        response = make_response({"score": "invalid"}, 200)

    response.headers.set("Content-Type", "application/json")
    response.headers.set("X-Content-Type-Options", "nosniff")

    return response

