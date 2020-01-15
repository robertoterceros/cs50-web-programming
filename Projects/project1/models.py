from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
db = SQLAlchemy(app)

class Books(db.Model):
    __tablename__="books"
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(80), nullable=False)
    title = db.Column(db.String(80), nullable=False)
    author = db.Column(db.String(80), nullable=False)
    year = db.Column(db.String(80), nullable=False)

class Users(db.Model):
     __tablename__ = "users"
     id = db.Column(db.Integer, primary_key=True)
     name = db.Column(db.String(80), nullable=False)
     email = db.Column(db.String(80), nullable=False)
     password = db.Column(db.String(180), nullable=False)

class reviews(db.Model):
     __tablename__ = "reviews"
     id = db.Column(db.Integer, primary_key=True)
     userid = db.Column(db.Integer, db.ForeignKey("users.id"), unique = True, nullable=False)
     bookid = db.Column(db.Integer, db.ForeignKey("books.id") , unique = True, nullable=False)
     comment = db.Column(db.Integer, nullable=False)
