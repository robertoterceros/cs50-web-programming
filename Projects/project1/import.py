import os
import csv

from flask import Flask, render_template, request
from models import *

# Check the environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

def main():
    # Create tables based on each table definition in `models.py`
    db.create_all()
    # NO SIRVE LA IMPORTACION. DEBE HACERSE DE OTRA MANERA
    # f = open("books.csv")
    # reader = csv.reader(f)
    # for isbn, title, author, year in reader:
    #     db.execute("INSERT INTO BOOKS (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
    #     {"isbn": isbn, "title": title, "author": author, "year": year}) # substitute values from CSV into SQL
    #     print(f"Added book titled {title} to the database.")
    # db.commit()

if __name__ == "__main__":
    with app.app_context():
        main()
