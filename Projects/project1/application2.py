# Este programa tiene el unico objetivo de crear las tablas definidas en models.py

from models import db
db.create_all()
