from sqlalchemy.orm import backref
from market import db

class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    budget = db.Column(db.Integer(), nullable=False, default=15)
    items = db.relationship('Champion', backref='owned_user', lazy=True)

class Champion(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    cost = db.Column(db.Integer(), nullable=False)
    power = db.Column(db.String(length=2), nullable=False)
    health = db.Column(db.String(length=2), nullable=False)
    description = db.Column(db.String(length=500), nullable=False, unique=True)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def __repr__(self):
        return f'Champion: {self.name}'