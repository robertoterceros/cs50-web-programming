from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Books(db.Model):
    __tablename__="books"
    isbn = db.Column(db.String, nullable=False, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    year = db.Column(db.String, nullable=False)

# class Users(db.Model):
#     __tablename__ = "users"
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String, nullable=False)
#     email = db.Column(db.String, nullable=False)
#     password = db.Column(db.String, nullable=False)
#
# class reviews(db.Model):
#     __tablename__ = "reviews"
#     id = db.Column(db.Integer, primary_key=True)
#     userid = db.Column(db.Integer, db.ForeignKey("users.id"), unique = True, nullable=False, )
#     bookid = db.Column(db.Integer, db.ForeignKey("books.id") , unique = True, nullable=False)
