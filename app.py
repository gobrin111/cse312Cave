import hashlib
import html

from bson import ObjectId
from flask_socketio import SocketIO, emit

from flask import Flask, request
from pymongo import MongoClient

from blueprints.root import root_bp
from blueprints.auth import auth_bp
from blueprints.chat import chat_bp
from blueprints.game import game_bp
# from blueprints.ws import ws_bp

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", transport=["websocket"])

app.register_blueprint(root_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(chat_bp)
app.register_blueprint(game_bp)
# app.register_blueprint(ws_bp)


mongo_client = MongoClient("mongo")
db = mongo_client["wurdle"]
user_collection = db["users"]
chat_collection = db["chat"]
like_collection = db["like"]
score_collection = db["score"]
@socketio.on("connect")
def handle_message():
    print("Client connected!")


@socketio.on("test")
def test_message(message):
    print(message)



@socketio.on("sendChat")
def handle_sendChat(message):
    escaped_message = html.escape(message)
    profile_pic = 'static/images/default.jpg'
    if "auth_token" in request.cookies:
        auth_token = request.cookies.get("auth_token")
        auth_token = hashlib.sha256(auth_token.encode('utf-8')).hexdigest()

        if user_collection.find_one({"auth_token": auth_token}):
            account = user_collection.find_one({"auth_token": auth_token})
            username = account.get("username")
            profile_pic = account.get("profile_pic")
            chat_collection.insert_one({"username": username, "message": escaped_message, "profile_pic": profile_pic})
            response = {
                'username': username,
                'message': message,
                'id': str(chat_collection.find_one({"username": username, "message": message})["_id"]),
                'from_user': False,
                'like_count': like_collection.count_documents({"message_id": str(chat_collection.find_one({"username": username, "message": message})["_id"])}),
                'profile_pic': profile_pic
            }
            emit('updateChat', response, broadcast=True, include_self=False)
            response['from_user'] = True
            emit('updateChat', response, to=request.sid)


@socketio.on("deleteMessage")
def deleteMessage(messageId):
    message_id = ObjectId(messageId)
    message = chat_collection.find_one({"_id": message_id})
    flag = False

    if "auth_token" in request.cookies:
        auth_token = request.cookies.get("auth_token")
        auth_token = hashlib.sha256(auth_token.encode('utf-8')).hexdigest()

        if user_collection.find_one({"auth_token": auth_token}):
            account = user_collection.find_one({"auth_token": auth_token})

            if message["username"] == account["username"]:
                chat_collection.delete_one({"_id": message_id})
                like_collection.delete_many({"message_id": messageId})
                socketio.emit('deleteUpdate', "message_"+messageId)



if __name__ == "__main__":
    socketio.run(app,host="0.0.0.0", port=8080, debug=True, use_reloader=False, log_output=True)
    # app.run(host="0.0.0.0", port=8080, debug=True)
