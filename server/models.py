from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import validates

from extensions import db, bcrypt


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    _password_hash = db.Column(
        "password_hash",
        db.String(255),
        nullable=False
    )

    # Relationship
    movies = db.relationship(
        "Movie",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    @hybrid_property
    def password_hash(self):
        raise AttributeError("Password hashes may not be viewed.")

    @password_hash.setter
    def password_hash(self, password):
        if not password or len(password) < 8:
            raise ValueError("Password must be at least 8 characters long.")

        self._password_hash = (
            bcrypt.generate_password_hash(password).decode("utf-8")
        )

    @validates("username")
    def validate_username(self, key, username):
        if not username:
            raise ValueError("Username is required.")

        username = username.strip()

        if len(username) < 3:
            raise ValueError("Username must be at least 3 characters long.")

        return username

    def authenticate(self, password):
        return bcrypt.check_password_hash(
            self._password_hash,
            password
        )

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
        }


class Movie(db.Model):
    __tablename__ = "movies"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(150), nullable=False)
    genre = db.Column(db.String(80), nullable=False)
    director = db.Column(db.String(100), nullable=False)
    release_year = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Float)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    user = db.relationship(
        "User",
        back_populates="movies"
    )

    @validates("title")
    def validate_title(self, key, value):
        if not value or not value.strip():
            raise ValueError("Title is required.")
        return value.strip()

    @validates("genre")
    def validate_genre(self, key, value):
        if not value or not value.strip():
            raise ValueError("Genre is required.")
        return value.strip()

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "genre": self.genre,
            "director": self.director,
            "release_year": self.release_year,
            "rating": self.rating,
            "user_id": self.user_id
        }
