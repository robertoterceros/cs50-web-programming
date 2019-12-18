import datetime

from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    now = datetime.datetime.now()
    memorial = (now.month == 4 and now.day ==  7)
    memorial = True
    return render_template("index.html", memorial=memorial)
