from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property
from marshmallow import Schema, fields, validate
from config import db, bcrypt

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    _password_hash = db.column(db.String)

    def __repr__(self):
        return f'<User {self.username}>'

class Workout(db.Model):
    __tablename__ = "workouts"
    id = db.column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    duration = db.Column(db.Integer)
    date = db.Column(db.Date)



