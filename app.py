import hashlib
import html
import os
import time

from bson import ObjectId
from flask_socketio import SocketIO, emit

from flask import Flask, request, redirect
from pymongo import MongoClient

from blueprints.root import root_bp
from blueprints.auth import auth_bp
from blueprints.chat import chat_bp
from blueprints.game import game_bp
from blueprints.board import board_bp

# from blueprints.ws import ws_bp

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", transport=["websocket"])
PORT = int(os.environ.get('PORT', 8080))

app.register_blueprint(root_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(chat_bp)
app.register_blueprint(game_bp)
app.register_blueprint(board_bp)
# app.register_blueprint(ws_bp)

MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://mongo:27017/wurdle')
mongo_client = MongoClient(MONGO_URI)
db = mongo_client["wurdle"]
user_collection = db["users"]
chat_collection = db["chat"]
like_collection = db["like"]
active_score_collection = db["score"]
board_score_collection = db["board"]

# keeps track of the timers of each user
user_timers = {}

active_users = set()


@socketio.on("connect")
def handle_message():
    print("Client connected!")
    active_users.add(request.sid)


@socketio.on("disconnect")
def handle_disconnect():
    # if a user disconnects, we have to delete their session id from the timers
    # just in case there might be an error
    active_users.remove(request.sid)
    if request.sid in user_timers.keys():
        del user_timers[request.sid]


@app.before_request
def before_request():
    if os.getenv('HEROKU') == '1':
        if request.headers.get('X-Forwarded-Proto', 'http') == 'http':
            url = request.url.replace('http://', 'https://', 1)
            return redirect(url, code=301)


@socketio.on("test")
def test_message(message):
    print(message)


# ---------------- Chat Stuff


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
                'like_count': like_collection.count_documents(
                    {"message_id": str(chat_collection.find_one({"username": username, "message": message})["_id"])}),
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
                socketio.emit('deleteUpdate', "message_" + messageId)


@socketio.on("likeMessage")
def likeMessage(messageId):
    if "auth_token" in request.cookies:
        user_account = user_collection.find_one(
            {"auth_token": hashlib.sha256(request.cookies["auth_token"].encode("utf-8")).hexdigest()})

        if user_account:
            username = user_account["username"]
            like = like_collection.find_one({"username": username, "message_id": messageId})
            if like:
                like_collection.delete_one({"username": username, "message_id": messageId})
            else:
                like_collection.insert_one({"username": username, "message_id": messageId})

            updated_like_count = like_collection.count_documents({"message_id": messageId})
            emit('likeMessage_client', {"num": updated_like_count, "message_id": "like_count_" + messageId},
                 broadcast=True)


# ---------------- timer stuff


@socketio.on("timer_start")
def timer_start():
    print("timer_start")
    sid = request.sid
    if sid in user_timers.keys():
        return
    if "auth_token" in request.cookies:
        auth_token = request.cookies.get("auth_token")
        auth_token = hashlib.sha256(auth_token.encode('utf-8')).hexdigest()

        if user_collection.find_one({"auth_token": auth_token}):
            account = user_collection.find_one({"auth_token": auth_token})
            username = account.get("username")
            active_score_collection.update_one({"username": username}, {"$set": {"score": 0}})
            socketio.emit('update_active_score', {"score": "invalid"}, to=request.sid)
    end_time = time.time() + 61
    user_timers[sid] = end_time
    # Start the countdown in a background task
    socketio.start_background_task(countdown_task, sid, end_time, request.cookies)


def countdown_task(sid, end_time, cookies):
    while True:
        # print("counting")
        # Calculate remaining time
        remaining_time = end_time - time.time()
        if sid not in active_users:
            break
        if remaining_time <= 0:
            socketio.emit('timer_update', {'remaining_time': 0}, to=sid)
            if "auth_token" in cookies:
                auth_token = cookies.get("auth_token")
                auth_token = hashlib.sha256(auth_token.encode('utf-8')).hexdigest()

                if user_collection.find_one({"auth_token": auth_token}):
                    account = user_collection.find_one({"auth_token": auth_token})
                    username = account.get("username")
                    profile_pic = account.get("profile_pic")
                    if active_score_collection.find_one({"username": username}):
                        new_score = active_score_collection.find_one({"username": username})["score"]
                        if board_score_collection.find_one({"username": username}):
                            board_score = board_score_collection.find_one({"username": username}).get("score")
                            if board_score < new_score:
                                board_score_collection.update_one({"username": username}, {"$set": {"score": new_score}})
                        else:
                            board_score_collection.insert_one({"username": username, "score": new_score, "profile_pic": profile_pic, "id": str(account.get("_id"))})
                        # active_score_collection.update_one({"username": username}, {"$set": {"score": new_score}})

                    else:
                        board_score_collection.insert_one({"username": username, "score": 0, "profile_pic": profile_pic})
                        # active_score_collection.insert_one({"username": username, "score": score})
                    if board_score_collection.find_one({"username": username}).get("profile_pic") != profile_pic:
                        board_score_collection.update_one({"username": username}, {"$set": {"profile_pic": profile_pic}})
            socketio.emit('update_leaderboard')
            del user_timers[sid]
            # socketio.emit('timer_expired', {'message': 'Time is up!'}, to=sid)
            break

        # Send remaining time to the client
        socketio.emit('timer_update', {'remaining_time': int(remaining_time)}, to=sid)
        socketio.sleep(1)  # Wait for 1 second between updates


# ---------------- game stuff


@socketio.on("send_score")
def send_score(data):
    score = data["score"]
    if "auth_token" in request.cookies:
        auth_token = request.cookies.get("auth_token")
        auth_token = hashlib.sha256(auth_token.encode('utf-8')).hexdigest()

        if user_collection.find_one({"auth_token": auth_token}):
            account = user_collection.find_one({"auth_token": auth_token})
            username = account.get("username")
            if active_score_collection.find_one({"username": username}):
                new_score = active_score_collection.find_one({"username": username})["score"] + score
                active_score_collection.update_one({"username": username}, {"$set": {"score": new_score}})

                socketio.emit('update_active_score', {"score": new_score}, to=request.sid)
                # response = make_response({"score": new_score}, 200)
            else:
                active_score_collection.insert_one({"username": username, "score": score})
    else:
        socketio.emit('update_active_score', {"score": "invalid"}, to=request.sid)
        # response = make_response({"score": "invalid"}, 200)


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=PORT, debug=False, use_reloader=False, log_output=True)
    # app.run(host="0.0.0.0", port=8080, debug=True)
