from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates


db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True,
        unique=True,
    )

    username = db.Column(
        db.String(50),
        nullable=False,
        unique=True,
    )

    _password_hash = db.Column(
        "password_hash",
        db.String(128),
        nullable=False,
    )

    tasks = db.relationship(
        "Task",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    @property
    def password_hash(self):    
        raise AttributeError("Password hashes may not be viewed.")

    @password_hash.setter
    def password_hash(self, password):
        if not password:
            raise ValueError("Password is required.")

        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long.")

        self._password_hash = (
            bcrypt.generate_password_hash(password)
            .decode("utf-8")
        )

    def authenticate(self, password):
        if not self._password_hash:
            return False
        
        return bcrypt.check_password_hash(
            self._password_hash,
            password,
        )


    @validates("username")
    def validate_username(self, key, username):
        if not username or not username.strip():
            raise ValueError("Username is required.")

        username = username.strip()

        if len(username) < 3:
            raise ValueError("Username must be at least 3 characters long.")

        if len(username) > 50:
            raise ValueError("Username must be at most 50 characters long.")

        return username 

    def __repr__(self):
        return f"<User {self.username}>"


class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(
        db.Integer,
        primary_key=True,
        unique=True,
    )

    title = db.Column(
        db.String(100),
        nullable=False,
    )

    description = db.Column(
        db.Text,
        nullable=False,
        default="",
    )

    completed = db.Column(
        db.Boolean,
        nullable=False,
        default=False,
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.now(),
    )

    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.now(),
        onupdate=db.func.now(),
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
    )

    user = db.relationship(
        "User",
        back_populates="tasks",
    )

    @validates("title")
    def validate_title(self, key, title):
        if not title or not title.strip():
            raise ValueError("Title is required.")

        title = title.strip()

        if len(title) < 3:
            raise ValueError("Title must be at least 3 characters long.")

        if len(title) > 100:
            raise ValueError("Title must be at most 100 characters long.")

        return title

    @validates("description")
    def validate_description(self, key, description):
        if description is None:
            return ""

        if not isinstance(description, str):
            raise ValueError("Description must be a string.")

        if len(description) > 1000:
            raise ValueError("Description must be at most 1000 characters long.")

        return description.strip()

    @validates("completed")
    def validate_completed(self, key, completed):
        if not isinstance(completed, bool):
            raise ValueError("Completed must be a boolean value.")

        return completed

    def __repr__(self):
        return f"<Task{self.id} {self.title}>"