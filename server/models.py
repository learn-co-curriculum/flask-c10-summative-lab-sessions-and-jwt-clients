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
    )

    username = db.Column(
        db.String(50),
        unique=True,
        nullable=False,
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
    def password(self):
        raise AttributeError(
            "Password cannot be viewed."
        )

    @password.setter
    def password(self, password):
        if not isinstance(password, str):
            raise ValueError(
                "Password must be a string."
            )

        if len(password) < 8:
            raise ValueError(
                "Password must contain at least 8 characters."
            )

        self._password_hash = (
            bcrypt.generate_password_hash(
                password
            ).decode("utf-8")
        )

    def authenticate(self, password):
        if not password:
            return False

        return bcrypt.check_password_hash(
            self._password_hash,
            password,
        )

    @validates("username")
    def validate_username(
        self,
        key,
        username,
    ):
        if not isinstance(username, str):
            raise ValueError(
                "Username must be a string."
            )

        username = username.strip()

        if len(username) < 3:
            raise ValueError(
                "Username must contain at least 3 characters."
            )

        if len(username) > 50:
            raise ValueError(
                "Username cannot exceed 50 characters."
            )

        return username

    def __repr__(self):
        return (
            f"<User {self.id}: "
            f"{self.username}>"
        )


class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(
        db.Integer,
        primary_key=True,
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
    def validate_title(
        self,
        key,
        title,
    ):
        if not isinstance(title, str):
            raise ValueError(
                "Title must be a string."
            )

        title = title.strip()

        if not title:
            raise ValueError(
                "Title is required."
            )

        if len(title) > 100:
            raise ValueError(
                "Title cannot exceed 100 characters."
            )

        return title

    @validates("description")
    def validate_description(
        self,
        key,
        description,
    ):
        if description is None:
            return ""

        if not isinstance(description, str):
            raise ValueError(
                "Description must be a string."
            )

        return description.strip()

    @validates("completed")
    def validate_completed(
        self,
        key,
        completed,
    ):
        if not isinstance(completed, bool):
            raise ValueError(
                "Completed must be true or false."
            )

        return completed

    def __repr__(self):
        return (
            f"<Task {self.id}: "
            f"{self.title}>"
        )