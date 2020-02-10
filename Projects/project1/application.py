# export FLASK_APP=application.py
# export FLASK_DEBUG=1
# export DATABASE_URL=postgres://msmtdlmfgaqhfo:320fb2dc2c2b09e5833f0a0a07e2823d441d02a0a999803102abd1b09d5d239c@ec2-107-20-243-220.compute-1.amazonaws.com:5432/d66l8esu194f6u
# Se detecto un problema con el login_required!!!!!!!!!!!!!!!!!!!!!!!



import os
import json
from flask import Flask, render_template, request, session, jsonify, flash, redirect
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.security import check_password_hash, generate_password_hash

import requests

from helpers import login_required, get_review

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
    return render_template("index.html")

@app.route("/login", methods = ['GET', 'POST'])
def login():
    session.clear()

    if request.method == "POST":
        if not request.form.get("username"):
            return render_template("error.html", message="Please enter the username")

        elif not request.form.get("password"):
            return render_template("error.html", message="Please enter the password")

        # Access the database for users
        username = request.form.get("username")
        rows = db.execute("SELECT * FROM USERS WHERE name = :name", {"name": username})

        output = rows.fetchone()

        # Be sure that the username exists
        if output == None:
            return render_template("error.html", message="Username not found. Please enter a valid username.")
        # Be sure that the password is correct
        if not check_password_hash(output[3], request.form.get("password")):
            return render_template("error.html", message="Incorrect password.")

        # Be sure and save the user that has logged in!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        session["id_user"] = output[0]
        session["name_user"] =  output[1]

        flash(f'Sucessfully login for {request.form.get("username")}', 'success')


        # Redirect user to home page
        return redirect("/")

    #If the user logged in using a link or via GET method redirect to the index page
    else:
        return render_template("login.html")


@app.route("/register", methods=['POST', 'GET']) #Debe admitir ambos metodos
def register():
    session.clear()

    # Ensure that the user doesn't try to register via GET
    if request.method == "POST":
        if not request.form.get("username"):
            return render_template("error.html", message="Please enter the username")

        if not request.form.get("password"):
            return render_template("error.html", message="Please provide the pasword")

            #Check if username already exists
        checkUser = db.execute("SELECT * FROM users WHERE name = :username",
        {"username":request.form.get("username")}).fetchone()

        if checkUser:
            return render_template("error.html", message="Username already exists")

            #Confirmation of password was entered
        elif not request.form.get("password"):
            return render_template("error.html", message="Please enter the password")

        elif not request.form.get("password2"):
            return render_template("error.html", message="Please confirm your password")

            #Confirmation of two passwords are equal
        elif not request.form.get("password") == request.form.get("password2"):
            return render_template("error.html", message="Password entered don't match")

            # Hash password
        hashedPassword = generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8)

            # Insert register into database and commit changes
        db.execute("INSERT INTO users (name, email, password) VALUES (:username, :email, :password)",
        {'username':request.form.get('username'), 'email':request.form.get('email'), 'password':hashedPassword})

            # Commit changes to database
        db.commit()

        flash(f'Account created for {request.form.get("username")}', 'success')

            #Redirect user to login page for first login
        return redirect("/login") #Diferencia entre redirect y render_template

    else:
        return render_template("register.html")


@app.route("/search", methods=['GET', 'POST'])
@login_required
def search():
    if not request.args.get("book"):
        print("Hello")
        return render_template("error.html", message="You must provide a book name")

    query = "%" + request.args.get("book") + "%"
    query = query.title()

    rows = db.execute("SELECT isbn, title, author, year FROM books WHERE isbn LIKE :query OR title LIKE :query OR author LIKE :query", {"query": query})

    if rows.rowcount == 0:
        return render_template("error.html", message="We can't find any book with the description entered")

    books = rows.fetchall()

    return render_template("results.html", books=books)


@app.route("/book/<isbn>", methods=["POST", "GET"])
#@login_required
def book(isbn):
    """ Save user review and load same page with reviews updates. """

    if request.method == "POST":

        user = session["id_user"]

        #Fetch form data
        rating = request.form.get("rating")
        comment = request.form.get("comment")

        # Convert to save into DB
        rating = int(rating)

        #Search book by ISBN
        row = db.execute("SELECT id FROM books WHERE isbn = :isbn", {"isbn": isbn})

        #Save id into variable
        bookid = row.fetchone()
        bookid = bookid[0]

        row2 = db.execute("SELECT * FROM reviews WHERE userid = :userid AND bookid = :bookid",
            {"userid": user,
            "bookid": bookid})
        userreview = row2.first()
        print("RESULT: ", userreview)

        if not userreview:
            db.execute("INSERT INTO reviews (userid, bookid, comment, rating) VALUES (:userid, :bookid, :comment, :rating)",
            {"userid": user,
            "bookid": bookid,
            "comment": comment,
            "rating": rating})

            db.commit()

        else:
            flash("You have already reviewed this book", "info")

        return redirect("/book/"+isbn)
    else:
        row = db.execute("SELECT isbn, title, author, year FROM books WHERE isbn= :isbn", {"isbn":isbn})

        bookInfo = row.fetchall()

        """ GOODREADS reviews"""
        query = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "pEhwApK0Hah2deHLG5Qjyg", "isbns": "9781632168146"})


        # Convert the response to json
        response = query.json()

        #Clean the JSON before passing it to the bookInfo List
        response = response["books"][0]

        #Append it as the second element on the list
        bookInfo.append(response)

        """ Users reviews """

        #Search bookid by isbn
        row = db.execute("SELECT id FROM books WHERE isbn = :isbn",
            {"isbn": isbn})

        # Save id into variable
        book = row.fetchone()
        book = book[0]



        # Fetch book reviews
        results = db.execute("SELECT users.name, comment, rating \
        FROM users \
        INNER JOIN reviews \
        ON users.id = reviews.userid \
        WHERE bookid = :book",
        {"book": book})

        reviews = results.fetchall()

        return render_template("book.html", bookInfo = bookInfo, reviews=reviews)

@app.route("/api/<isbn>")
#@login_required
def api_call(isbn):
    # Para bordear el impedimento de isbn terminado en X se hace lo siguiente:
    isbn2 = isbn
    if isbn2[-1]=="X":
        isbn2 = isbn2[:-1]
    isbn2 = f"%{isbn2}%".lower()
    check_isbn = db.execute("SELECT * FROM books WHERE isbn LIKE :isbn", {"isbn": isbn2}).fetchone()
    if check_isbn is None:
        return jsonify(
            {
                "error_code": 404,
                "error_message": "Not Found",
                "isbn": isbn
            }
        ), 404

    else:
        # Get info from the books table and then add isbn again
        result = db.execute("SELECT title, author, year FROM books WHERE isbn LIKE :isbn", {"isbn": isbn2}).fetchone()
        book_data = dict(result)
        book_data['isbn'] = isbn

        #Query Goodreads API for data on book ratings

        gr_reviews_count, gr_average_rating = get_review(isbn)

        book_data['review_count'] = gr_reviews_count
        book_data['average_score'] = float(gr_average_rating)

        return jsonify(book_data)


@app.route("/logout")
def logout():
    #Forget the session
    session.clear()
    #Redirect to index.html
    return render_template("index.html")
