from flask import Flask, render_template, send_from_directory, make_response, request, redirect, url_for
from pymongo import MongoClient
from bson import ObjectId
import json
import html
import bcrypt
import hashlib
import uuid

app = Flask(__name__)

mongo_client = MongoClient("mongo")
db = mongo_client["wurdle"]
user_collection = db["users"]
chat_collection = db["chat"]


# Root path
@app.route("/")
def index():
    auth_token = request.cookies.get('auth_token')
    user = None
    if auth_token:
        user = user_collection.find_one({"auth_token": hashlib.sha256(auth_token.encode('utf-8')).hexdigest()})

    username = user["username"] if user else None

    response = make_response(render_template("index.html", username=username))
    response.headers.set("Content-Type", "text/html")
    response.headers.set("X-Content-Type-Options", "nosniff")
    return response


@app.route("/login.html")
def login_html():
    response = make_response(render_template("login.html"))
    response.headers.set("Content-Type", "text/html")
    response.headers.set("X-Content-Type-Options", "nosniff")
    return response


@app.route("/register.html")
def register_html():
    response = make_response(render_template("register.html"))
    response.headers.set("Content-Type", "text/html")
    response.headers.set("X-Content-Type-Options", "nosniff")
    return response


@app.route("/static/css/styles.css")
def css():
    response = make_response(send_from_directory("static/css", "styles.css"))
    response.headers.set("Content-Type", "text/css")
    response.headers.set("X-Content-Type-Options", "nosniff")
    return response


@app.route("/static/css/credentials.css")
def credentials_style():
    response = make_response(send_from_directory("static/css", "credentials.css"))
    response.headers.set("Content-Type", "text/css")
    response.headers.set("X-Content-Type-Options", "nosniff")
    return response


@app.route("/static/js/script.js")
def js():
    response = make_response(send_from_directory("static/js", "script.js"))
    response.headers.set("Content-Type", "text/javascript")
    response.headers.set("X-Content-Type-Options", "nosniff")
    return response


@app.route("/static/js/wordFlip.js")
def wordFlip_js():
    response = make_response(send_from_directory("static/js", "wordFlip.js"))
    response.headers.set("Content-Type", "text/javascript")
    response.headers.set("X-Content-Type-Options", "nosniff")
    return response


@app.route("/static/images/wordle-favicon.ico")
def favicon():
    response = make_response(send_from_directory("static/images", "wordle-favicon.ico"))
    response.headers.set("Content-Type", "image/x-icon")
    response.headers.set("X-Content-Type-Options", "nosniff")
    return response


@app.route("/static/images/logo.png")
def image():
    response = make_response(send_from_directory("static/images", "logo.png"))
    response.headers.set("Content-Type", "image/png")
    response.headers.set("X-Content-Type-Options", "nosniff")
    return response


# Register Code
def hash_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')


def check_password(hashed_password, password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))


def validate_password(password):
    special = {'!', '@', '#', '$', '%', '^', '&', '(', ')', '-', '_', '='}
    if len(password) < 8:
        return False
    lower = False
    upper = False
    number = False
    specialChar = False
    for character in password:
        if character.islower():
            lower = True
        elif character.isupper():
            upper = True
        elif character.isdigit():
            number = True
        elif character in special:
            specialChar = True
        else:
            return False
    return lower and upper and number and specialChar


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    password_confirm = data.get('password_confirm')
    if not validate_password(password) or password != password_confirm:
        response = make_response(json.dumps({"error": "Invalid Password"}), 403)
        response.headers.set("Content-Type", "application/json")
        response.headers.set("X-Content-Type-Options", "nosniff")
        return response

    # if username exists
    if user_collection.find_one({"username": username}):
        response = make_response(json.dumps({"error": "Username Already Taken"}), 403)
        response.headers.set("Content-Type", "application/json")
        response.headers.set("X-Content-Type-Options", "nosniff")
        return response

    hashed_password = hash_password(password)
    user_collection.insert_one({"username": username, "password": hashed_password})

    response = make_response(json.dumps({"message": "Register Successful"}), 200)
    response.headers.set("Content-Type", "application/json")
    response.headers.set("X-Content-Type-Options", "nosniff")
    return response


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = user_collection.find_one({"username": username})
    if not user or not check_password(user['password'], password):
        response = make_response(json.dumps({"error": "Invalid username or password"}), 403)
        response.headers.set("Content-Type", "application/json")
        response.headers.set("X-Content-Type-Options", "nosniff")
        return response

    token = str(uuid.uuid4())
    hashed_token = hashlib.sha256(token.encode('utf-8')).hexdigest()
    user_collection.update_one({"username": username}, {"$set": {"auth_token": hashed_token}})

    response = make_response(json.dumps({"message": "Login successful"}), 200)
    response.headers.set("Content-Type", "application/json")
    response.headers.set("X-Content-Type-Options", "nosniff")
    response.set_cookie('auth_token', token, max_age=3600, httponly=True)

    return response


@app.route('/logout', methods=['POST'])
def logout():
    auth_token = request.cookies.get("auth_token")

    if auth_token:
        user_collection.update_one({"auth_token": hashlib.sha256(auth_token.encode('utf-8')).hexdigest()},
                                   {"$set": {"auth_token": None}})

    response = make_response(redirect(url_for('index')))
    response.set_cookie('auth_token', '', max_age=0, httponly=True)
    return response


@app.route('/chat-messages', methods=['POST'])
def post_message():  # this is done
    data = request.get_json()
    message = html.escape(data["message"])
    print(message)
    response = make_response(json.dumps({"message": "Message Posted"}), 200)
    response.headers.set("Content-Type", "application/json")
    response.headers.set("X-Content-Type-Options", "nosniff")
    if "auth_token" in request.cookies:
        auth_token = request.cookies.get("auth_token")
        auth_token = hashlib.sha256(auth_token.encode('utf-8')).hexdigest()
        if user_collection.find_one({"auth_token": auth_token}):
            account = user_collection.find_one({"auth_token": auth_token})
            username = account.get("username")
            print(username)
            print("posted something")
            chat_collection.insert_one({"username": username, "message": message})
    else:
        response = make_response(json.dumps({"message": "no account"}), 403)
    return response


@app.route('/chat-messages', methods=['GET'])
def get_messages(): #done
    messages = chat_collection.find({})
    message_display = []
    for message in messages:
        print("this is the issue")
        print(message)
        background_color = 'white'
        if "token" in request.cookies:
            if user_collection.find_one(
                    {"token": hashlib.sha256(request.cookies["token"].encode("utf-8")).hexdigest()}):
                if user_collection.find_one(
                        {"token": hashlib.sha256(request.cookies["token"].encode("utf-8")).hexdigest()})["username"] == \
                        message["username"]:
                    background_color = 'green'
        message_display.append({
            "message": message["message"],
            "username": message["username"],
            "id": str(message["_id"]),
            "color": background_color
        })
    message_display = json.dumps(message_display)
    response = make_response(message_display, 200)
    response.headers.set("Content-Type", "application/json")
    response.headers.set("X-Content-Type-Options", "nosniff")
    return response


@app.route('/chat-messages/<message_id>', methods=['POST'])
def delete_message(message_id):  # this is done
    # message_id = ObjectId(request.path[15:len(request.path)])
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
                flag = True
    if flag:
        response = make_response(json.dumps({"message": "post deleted"}), 204)
    else:
        response = make_response(json.dumps({"message": "action not possible"}), 403)
    response.headers.set("X-Content-Type-Options", "nosniff")
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
