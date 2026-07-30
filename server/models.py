from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property
from marshmallow import Schema, fields, validate
from config import db, bcrypt

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    _password_hash = db.column(db.String, nullable=False)
    workouts = db.relationship("Workout", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f'<User {self.username}>'

class Workout(db.Model):
    __tablename__ = "workouts"
    id = db.column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.Integer, ForeignKey("users.id"), nullable=False)
    user = db.Relationship("User", back_populates="workouts")



