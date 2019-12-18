from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello World"

@app.route("/david")
def david():
    return "Hello david"

@app.route("/roberto")
def roberto():
    return "Hello, roberto"
