from flask import Flask, render_template, send_from_directory, make_response

app = Flask(__name__)


# Root path
@app.route("/")
def index():
    response = make_response(render_template("index.html"))
    response.headers.set("Content-Type", "text/html")
    response.headers.set("X-Content-Type-Options", "nosniff")
    return response


@app.route("/login.html")
def login_html():
    response = make_response(render_template("login.html"))
    response.headers.set("Content-Type", "text/html")
    response.headers.set("X-Content-Type-Options", "nosniff")
    return response


@app.route("/static/css/styles.css")
def css():
    response = make_response(send_from_directory("static/css", "styles.css"))
    response.headers.set("Content-Type", "text/css")
    response.headers.set("X-Content-Type-Options", "nosniff")
    return response


@app.route("/static/css/login.css")
def login_style():
    response = make_response(send_from_directory("static/css", "login.css"))
    response.headers.set("Content-Type", "text/css")
    response.headers.set("X-Content-Type-Options", "nosniff")
    return response


@app.route("/static/js/script.js")
def js():
    response = make_response(send_from_directory("static/js", "script.js"))
    response.headers.set("Content-Type", "text/javascript")
    response.headers.set("X-Content-Type-Options", "nosniff")
    return response


@app.route("/static/images/red_tercel.ico")
def favicon():
    response = make_response(send_from_directory("static/images", "red_tercel.ico"))
    response.headers.set("Content-Type", "image/x-icon")
    response.headers.set("X-Content-Type-Options", "nosniff")
    return response


@app.route("/static/images/image_placeholder.png")
def image():
    response = make_response(send_from_directory("static/images", "image_placeholder.png"))
    response.headers.set("Content-Type", "image/png")
    response.headers.set("X-Content-Type-Options", "nosniff")
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
