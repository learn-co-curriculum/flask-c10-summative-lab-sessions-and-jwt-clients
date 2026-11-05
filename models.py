"""Database models: User and Note (a note belongs to exactly one user)."""
from datetime import datetime

from sqlalchemy.orm import validates

from config import bcrypt, db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    # unique=True makes the username a valid identifier at the database level.
    username = db.Column(db.String(50), unique=True, nullable=False)
    _password_hash = db.Column(db.String(128), nullable=False)

    # Deleting a user also deletes their notes.
    notes = db.relationship("Note", back_populates="user", cascade="all, delete-orphan")

    @property
    def password_hash(self):
        # Hashes are write-only so they can never leak through the API.
        raise AttributeError("Password hashes may not be viewed.")

    @password_hash.setter
    def password_hash(self, password):
        self._password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def authenticate(self, password):
        """Return True if `password` matches the stored bcrypt hash."""
        return bcrypt.check_password_hash(self._password_hash, password)

    @validates("username")
    def validate_username(self, key, value):
        if not isinstance(value, str) or len(value.strip()) < 3:
            raise ValueError("Username must be at least 3 characters.")
        return value.strip()

    def __repr__(self):
        return f"<User {self.id} {self.username}>"


class Note(db.Model):
    __tablename__ = "notes"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False, default="general")
    is_pinned = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    user = db.relationship("User", back_populates="notes")

    def __repr__(self):
        return f"<Note {self.id} {self.title!r} user={self.user_id}>"