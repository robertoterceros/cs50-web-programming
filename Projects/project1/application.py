# export FLASK_APP=application.py
# export FLASK_DEBUG=1
# export DATABASE_URL=postgres://msmtdlmfgaqhfo:320fb2dc2c2b09e5833f0a0a07e2823d441d02a0a999803102abd1b09d5d239c@ec2-107-20-243-220.compute-1.amazonaws.com:5432/d66l8esu194f6u

import os, json
from werkzeug.security import check_password_hash, generate_password_hash

from flask import Flask, render_template, request, session, jsonify, flash, redirect
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import requests

from helpers import login_required

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

        # Be sure and save the user that has logged in
        session["id_user"] = output[0]
        session["name_user"] =  output[1]

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

            #Confirmation that the user has created an account (send a confirmation email)


            # Hash password
        hashedPassword = generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8)

            # Insert register into database and commit changes
        db.execute("INSERT INTO users (name, email, password) VALUES (:username, :email, :password)",
        {'username':request.form.get('username'), 'email':request.form.get('email'), 'password':hashedPassword})

            # Commit changes to database
        db.commit()

            #Redirect user to login page for first login
        return redirect("/login") #Diferencia entre redirect y render_template

    else:
        return render_template("register.html")


@app.route("/search", methods=["GET"])
@login_required
def search():
    if not requests.args.get("book"):
        return render_template("error.html", message="Please enter the book")

    query = "%" + request.args.get("book") + "%"
    query = query.title()

    rows = db.execute("SELECT isbn, title, author, year FROOM books WHERE isbn LIKE :query OR title LIKE :query OR author LIKE :query", {"query": query})

    if rows.rowcount == 0:
        return render_template("error.html", message="We can't find any book with the description entered")

    books = rows.fetchall()

    return render_template("results.html", books=books)


@app.route("/book/<isbn>", methods=["POST", "GET"])
@login_required
def book(isbn):
    """ Save user review and load same page with reviews updates. """

    if request.method == "POST":

        user = session["id_user"]

        #Fetch form data
        rating = request.form.get("rating")
        comment = request.form.get("comment")

        #Search bok by ISBN
        row = db.execute("SELECT id FROM books WHERE isbn = :isbn", {"isbn": isbn})

        #Save id into variable
        bookId = row.fetchone()
        bookId = bookId[0]

        row2 = db.execute("SELECT * FROM reviews WHERE id_user = :id_user AND book_id = :book_id",
            {"id_user": user,
            "book_id": bookId})

        if row2.rowcount == 1:
            return redirect("/book/" + isbn)

        # Convert to save into DB
        rating = int(rating)

        db.execute("INSER INTO reviews (id_user, bookId, comment, rating) VALUES (:id_user, :bookId, :comment, :rating)",
        {"id_user": user,
        "bookId": bookId,
        "comment": comment,
        "rating": rating})

        db.commit()

        return redirect("/book/"+isbn)
    else:
        row = db.execute("SELECT isbn, title, author, year FROM books WHERE isbn= :isbn", {"isbn":isbn})

        bookInfo = row.fetchall()

        """ GOODREADS reviews"""

        # Read API key from env variable
        key = os.getenv("GOODREADS_KEY")

        #Query the api with key and ISBN as parameters
        query = requests.get("https://www.goodreads.com/book/review_counts.json",
        params={"key": key, "isbn": isbn})

        # Convert the response to json
        response = query.json()

        #Clean the JSON before passing it to the bookInfo List
        response = response["books"][0]

        #Append it as the second element on the list
        bookInfo.append(response)

        """ Users reviews """

        #Search book_id by isbn
        row = db.execute("SELECT id FROM books WHERE isbn = :isbn",
            {"isbn": isbn})

        # Save id into variable
        book = row.fetchone()
        book = book[0]

        # Fetch book reviews
        results = db.execute("SELECT users.username, comment, rating, to_char(time, 'DD Mon YY - HH24:MI:SS') as time \
        FROM users \
        INNER JOIN reviews \
        ON users.id = reviews.user_id \
        WHERE book_id = :book \
        ORDER BY time",
        {"book", book})

    reviews = results.fetchall()

    return render_template("book.html", bookInfo = bookInfo, reviews = reviews)

@app.route("/api/<isbn>", methods = ['GET'])
@login_required
def api_call(isbn):

    row = db.execute("SELECT title, author, year, isbn, \
        COUNT(reviews.id) as review_count, \
        AVG(reviews.rating) as average_score \
        FROM books \
        INNER JOIN reviews \
        ON books.id = reviews.book_id \
        WHERE isbn= :isbn \
        GROUP BY title, author, year, isbn",
        {"isbn": isbn})

    #Error checking
    if row.rowcount != 1:
        return jsonify({"Error": "Invalid book ISBN"}), 422

    # Fetch results from RowProxy
    tmp = row.fetchone()

    #Convert to dict
    result = dict(tmp.items())

    #Round AVG Score to 2 decimal
    result['average_score'] = float('%.2f'%(result['average_score']))

    return jsonify(result)



@app.route("/logout")
def logout():
    #Forget the session
    session.clear()
    #Redirect to index.html
    return render_template("index.html")
