from flask_socketio import SocketIO

from flask import Flask, Blueprint

ws_bp = Blueprint('ws_bp', __name__)
socketio = SocketIO()


@socketio.on("connect")
def handle_message():
    print("Client connected!")


@socketio.on("test")
def test_message(message):
    print(message)




