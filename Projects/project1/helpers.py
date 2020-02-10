from flask import redirect, render_template, request, session
from functools import wraps
import requests

def login_required(f):
    """ Decorates routes to require login """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("id_user") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def get_review(isbn):
    developer_key = 'pEhwApK0Hah2deHLG5Qjyg'
    query = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "pEhwApK0Hah2deHLG5Qjyg", "isbns": "9781632168146"})
    response = query.json()
    response = response["books"][0]
    gr_reviews_count = response['reviews_count']
    gr_average_rating = response['average_rating']
    return gr_reviews_count, gr_average_rating
