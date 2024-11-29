from flask import Blueprint, render_template, send_from_directory, make_response, request
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import hashlib
import os

root_bp = Blueprint("root", __name__)

mongo_uri = os.getenv('MONGO_URI')
mongo_client = MongoClient(mongo_uri, server_api=ServerApi('1'), ssl=True)
db = mongo_client["wurdle"]
user_collection = db["users"]
chat_collection = db["chat"]
like_collection = db["like"]
score_collection = db["score"]

@root_bp.route("/")
def index():
    auth_token = request.cookies.get('auth_token')
    user = None
    if auth_token:
        user = user_collection.find_one({"auth_token": hashlib.sha256(auth_token.encode('utf-8')).hexdigest()})

    username = user["username"] if user else None
    profile_pic = user["profile_pic"] if user else 'static/images/logo.png'
    print("profile" + profile_pic)

    response = make_response(render_template("index.html", username=username, profile_pic=profile_pic))
    response.headers.set("Content-Type", "text/html")
    response.headers.set("X-Content-Type-Options", "nosniff")
    return response


@root_bp.route("/login.html")
def login_html():
    response = make_response(render_template("login.html"))
    response.headers.set("Content-Type", "text/html")
    response.headers.set("X-Content-Type-Options", "nosniff")
    return response


@root_bp.route("/register.html")
def register_html():
    response = make_response(render_template("register.html"))
    response.headers.set("Content-Type", "text/html")
    response.headers.set("X-Content-Type-Options", "nosniff")
    return response


@root_bp.route("/static/css/style.css")
def css():
    response = make_response(send_from_directory("static/css", "style.css"))
    response.headers.set("Content-Type", "text/css")
    response.headers.set("X-Content-Type-Options", "nosniff")
    return response


@root_bp.route("/static/css/credentials.css")
def credentials_style():
    response = make_response(send_from_directory("static/css", "credentials.css"))
    response.headers.set("Content-Type", "text/css")
    response.headers.set("X-Content-Type-Options", "nosniff")
    return response


@root_bp.route("/static/js/script.js")
def js():
    response = make_response(send_from_directory("static/js", "script.js"))
    response.headers.set("Content-Type", "text/javascript")
    response.headers.set("X-Content-Type-Options", "nosniff")
    return response


@root_bp.route("/static/js/wordFlip.js")
def wordFlip_js():
    response = make_response(send_from_directory("static/js", "wordFlip.js"))
    response.headers.set("Content-Type", "text/javascript")
    response.headers.set("X-Content-Type-Options", "nosniff")
    return response


@root_bp.route("/static/js/game.js")
def game_js():
    response = make_response(send_from_directory("static/js", "game.js"))
    response.headers.set("Content-Type", "text/javascript")
    response.headers.set("X-Content-Type-Options", "nosniff")
    return response


@root_bp.route("/static/images/wordle-favicon.ico")
def favicon():
    response = make_response(send_from_directory("static/images", "wordle-favicon.ico"))
    response.headers.set("Content-Type", "image/x-icon")
    response.headers.set("X-Content-Type-Options", "nosniff")
    return response


@root_bp.route("/static/images/logo.png")
def image():
    response = make_response(send_from_directory("static/images", "logo.png"))
    response.headers.set("Content-Type", "image/png")
    response.headers.set("X-Content-Type-Options", "nosniff")
    return response
