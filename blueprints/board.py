from flask import Blueprint, make_response, request
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from bson import ObjectId
import json
import html
import hashlib
import os
board_bp = Blueprint("board", __name__)

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


@board_bp.route('/board-entries', methods=['GET'])
def get_messages():
    messages = board_score_collection.find({}).sort("score", -1)
    entry_display = []
    for message in messages:
        entry_display.append({
            "score": message["message"],
            "username": message["username"],
            "profile_pic": message["profile_pic"],
            "id": str(message["_id"]),

        })

    entry_display = json.dumps(entry_display)
    response = make_response(entry_display, 200)
    response.headers.set("Content-Type", "application/json")
    response.headers.set("X-Content-Type-Options", "nosniff")

    return response