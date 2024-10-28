from flask import Blueprint, make_response, request, redirect, url_for
from pymongo import MongoClient
import json
import bcrypt
import hashlib
import uuid

auth_bp = Blueprint("auth", __name__)

mongo_client = MongoClient("mongo")
db = mongo_client["wurdle"]
user_collection = db["users"]
chat_collection = db["chat"]
like_collection = db["like"]


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


@auth_bp.route('/register', methods=['POST'])
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


@auth_bp.route('/login', methods=['POST'])
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


@auth_bp.route('/logout', methods=['POST'])
def logout():
    auth_token = request.cookies.get("auth_token")

    if auth_token:
        user_collection.update_one({"auth_token": hashlib.sha256(auth_token.encode('utf-8')).hexdigest()},
                                   {"$set": {"auth_token": None}})

    response = make_response(redirect(url_for('root.index')))
    response.set_cookie('auth_token', '', max_age=0, httponly=True)
    return response
