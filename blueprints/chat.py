from flask import Blueprint, make_response, request
from pymongo import MongoClient
from bson import ObjectId
import json
import html
import hashlib

chat_bp = Blueprint("chat", __name__)

mongo_client = MongoClient("mongo")
db = mongo_client["wurdle"]
user_collection = db["users"]
chat_collection = db["chat"]
like_collection = db["like"]


@chat_bp.route('/chat-messages', methods=['POST'])
def post_message():

    data = request.get_json()
    message = html.escape(data["message"])
    response = make_response(json.dumps({"message": "Message Posted"}), 200)
    response.headers.set("Content-Type", "application/json")
    response.headers.set("X-Content-Type-Options", "nosniff")

    if "auth_token" in request.cookies:
        auth_token = request.cookies.get("auth_token")
        auth_token = hashlib.sha256(auth_token.encode('utf-8')).hexdigest()

        if user_collection.find_one({"auth_token": auth_token}):
            account = user_collection.find_one({"auth_token": auth_token})
            username = account.get("username")
            chat_collection.insert_one({"username": username, "message": message})

    else:
        response = make_response(json.dumps({"message": "no account"}), 403)

    return response


@chat_bp.route('/chat-messages', methods=['GET'])
def get_messages():
    messages = chat_collection.find({})
    message_display = []

    for message in messages:
        from_user = False
        if "auth_token" in request.cookies:
            if user_collection.find_one({"auth_token": hashlib.sha256(request.cookies["auth_token"].encode("utf-8")).hexdigest()}):
                if user_collection.find_one({"auth_token": hashlib.sha256(request.cookies["auth_token"].encode("utf-8")).hexdigest()})["username"] == message["username"]:
                    from_user = True

        message_display.append({
            "message": message["message"],
            "username": message["username"],
            "id": str(message["_id"]),
            "from_user": from_user,
            "like_count": like_collection.count_documents({"message_id": str(message["_id"])})
        })

    message_display = json.dumps(message_display)
    response = make_response(message_display, 200)
    response.headers.set("Content-Type", "application/json")
    response.headers.set("X-Content-Type-Options", "nosniff")

    return response


@chat_bp.route('/chat-messages/<message_id>', methods=['POST'])
def delete_message(message_id):
    id_message = message_id # just stores the none ObjectId of the message_id for later use
    message_id = ObjectId(message_id)
    message = chat_collection.find_one({"_id": message_id})
    flag = False

    if "auth_token" in request.cookies:
        auth_token = request.cookies.get("auth_token")
        auth_token = hashlib.sha256(auth_token.encode('utf-8')).hexdigest()

        if user_collection.find_one({"auth_token": auth_token}):
            account = user_collection.find_one({"auth_token": auth_token})

            if message["username"] == account["username"]:
                chat_collection.delete_one({"_id": message_id})
                like_collection.delete_many({"message_id": id_message})
                flag = True

    if flag:
        response = make_response(json.dumps({"message": "post deleted"}), 204)
    else:
        response = make_response(json.dumps({"message": "action not possible"}), 403)

    response.headers.set("X-Content-Type-Options", "nosniff")
    return response


@chat_bp.route('/chat-messages/like/<message_id>', methods=['POST'])
def like_message(message_id):
    # this function is triggered when the user clicks on the like bottom on a comment
    #  messageid of the liked message is sent
    response = make_response(json.dumps({"message": "post_liked"}), 204)

    if "auth_token" not in request.cookies:
        response = make_response(json.dumps({"message": "action not possible"}), 403)
    else:
        user_account = user_collection.find_one(
            {"auth_token": hashlib.sha256(request.cookies["auth_token"].encode("utf-8")).hexdigest()})

        if user_account:
            username = user_account["username"]
            like = like_collection.find_one({"username": username, "message_id": message_id})
            if like:
                like_collection.delete_one({"username": username, "message_id": message_id})
            else:
                like_collection.insert_one({"username": username, "message_id": message_id})

            updated_like_count = like_collection.count_documents({"message_id": message_id})

            response = make_response(json.dumps({"message": "post_liked", "like_count": updated_like_count}),200)
        else:
            response = make_response(json.dumps({"message": "action not possible"}), 403)

    response.headers.set("X-Content-Type-Options", "nosniff")
    return response
