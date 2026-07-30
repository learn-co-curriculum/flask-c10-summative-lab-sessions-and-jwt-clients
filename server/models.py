from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property
from marshmallow import Schema, fields, validate
from config import db, bcrypt

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    _password_hash = db.Column(db.String, nullable=False)
    workouts = db.relationship("Workout", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f'<User {self.username}>'

    @hybrid_property
    def password_hash(self):
        raise AttributeError("Password hashes cannot be viewed!")

    @password_hash.setter
    def password_hash(self, password):
        password_hash = bcrypt.generate_password_hash(password.encode('utf-8'))
        self._password_hash = password_hash.decode('utf-8')

    def authenticate(self, password):
        return bcrypt.check_password_hash(
            self._password_hash, password.encode('utf-8')
        )


    @validates("Username")
    def validate_username(self, key, username):
        if not username:
            raise ValueError("Username is required")
        if len(username) < 3:
            raise ValueError("Username must be at least 3 characters.")
        return username

class Workout(db.Model):
    __tablename__ = "workouts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.Relationship("User", back_populates="workouts")
    def __repr__(self):
        return f'<Workout {self.title} {self.duration} {self.date}>'

    @validates("title")
    def validate_title(self, key, title):
        if not title:
            raise ValueError("Title is required.")
        return title

    @validates("duration")
    def validates_duration(self, key, duration):
        if duration <= 0:
            raise ValueError("Duration must be greater than zero.")
        return duration



class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)


class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    duration = fields.Int(required=True)
    date = fields.Date(required=True)
    user_id = fields.Int(dump_only=True)

user_schema = UserSchema()
users_schema = UserSchema(many=True)
workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)

