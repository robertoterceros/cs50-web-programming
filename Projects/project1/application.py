# export FLASK_APP=application.py
# export FLASK_DEBUG=1
# export DATABASE_URL=postgres://msmtdlmfgaqhfo:320fb2dc2c2b09e5833f0a0a07e2823d441d02a0a999803102abd1b09d5d239c@ec2-107-20-243-220.compute-1.amazonaws.com:5432/d66l8esu194f6u

import os

from flask import Flask, render_template, request, session
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import requests

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

@app.route("/login", methods = ['GET', 'POST '])
def login():
    session.clear()
    username = request.form.get("username")

    if request.method == "POST":
        if not request.form.get("username"):
            return render_template("error.html", message="Please enter the username")

        elif not request.form.get("password"):
            return render_template("error.html", message="Please enter the password")

        # Access the database for users
        rows = db.execute("SELECT * FROM USERS WHERE username = :username", {"username": username})

        results = rows.fetchone()

        # Be sure that the username exists and password in correct

        # Be sure and save the user that has logged in

        # Redirect user to home page

    #If the user logged in using a link or via GET method redirect to the index page
    else:
        return render_template("index.html")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register")
def register():
    session.clear()

    # Ensure that the user doesn't try to register via GET
    if request.method == "POST":
        if not request.form.get("username"):
            return render_template("error.html", message="Please enter the username")

        if not request.form.get("password"):
            return render_template("error.html", message="Please provide the pasword")

            #Check if username already exists

            #Confirmation of password was entered

            #Confirmation of two passwords are equal

            #Confirmation that the user has created an account (send a confirmation email)

            # Hash password

            # Insert register into database and commit changes

            #Redirect user to login page for first login
            return redirect("/login") #Diferencia entre redirect y render_template

        else:
            return render_template("register.html")


@app.route("/search")
def search():
    #TODO

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/logout")
def logout():
    #Forget the session
    session.clear()
    #Redirect to index.html
    return render_template("index.html")
