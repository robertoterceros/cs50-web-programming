# export FLASK_APP=application.py
# export FLASK_DEBUG=1
# export DATABASE_URL=postgres://msmtdlmfgaqhfo:320fb2dc2c2b09e5833f0a0a07e2823d441d02a0a999803102abd1b09d5d239c@ec2-107-20-243-220.compute-1.amazonaws.com:5432/d66l8esu194f6u

import os

from flask import Flask, render_template, request, session
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return render_template(index.html)

@app.route("/register")
def register():
    return render_template(register.html)

@app.route("/login")
def login():
    return render_template(login.html)

@app.route("/logout")
def logout():
    return render_template(logout.html)
