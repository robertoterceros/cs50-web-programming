# . venv/bin/activate

from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hola Mundo'


#http://127.0.0.1:8000/params?params1=Eduardo_Ismael&params2=test_dos
@app.route('/<string:name>')
def hello(name):
    return f"hello, {name}!"
