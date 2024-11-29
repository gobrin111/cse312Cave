from flask import Flask

from blueprints.root import root_bp
from blueprints.auth import auth_bp
from blueprints.chat import chat_bp
from blueprints.game import game_bp

app = Flask(__name__)

app.register_blueprint(root_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(chat_bp)
app.register_blueprint(game_bp)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
