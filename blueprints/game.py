from flask import Blueprint, make_response, request
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from bson import ObjectId
import json
import html
import hashlib
import os

game_bp = Blueprint("game", __name__)

mongo_uri = os.getenv('MONGO_URI')
client = MongoClient(mongo_uri, server_api=ServerApi('1'))
db = mongo_client["wurdle"]
user_collection = db["users"]
chat_collection = db["chat"]
like_collection = db["like"]
score_collection = db["score"]


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
            if score_collection.find_one({"username": username}):
                new_score = score_collection.find_one({"username": username})["score"] + score
                score_collection.update_one({"username": username}, {"$set": {"score": new_score}})
                response = make_response({"score": new_score}, 200)
            else:
                score_collection.insert_one({"username": username, "score": score})
    else:
        response = make_response({"score": "invalid"}, 200)

    response.headers.set("Content-Type", "application/json")
    response.headers.set("X-Content-Type-Options", "nosniff")

    return response

