

from flask import current_app, request, url_for
from app import db



class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), indexed=True)


    def __init__(self, name):
        self.name = name


