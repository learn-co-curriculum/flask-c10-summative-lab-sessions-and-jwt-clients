"""
models.py
---------
Defines all SQLAlchemy database models and Marshmallow serialisation schemas.

Models:
    User  — Represents a registered user account.
    Note  — Represents a personal note owned by a user.

Schemas:
    UserSchema — Serialises a User object to a JSON-safe dictionary.
    NoteSchema — Serialises a Note object to a JSON-safe dictionary.
"""

from datetime import datetime

from marshmallow import Schema, fields
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import validates

from config import db, bcrypt


# ── User model ────────────────────────────────────────────────────────────────

class User(db.Model):
    __tablename__ = 'users'

    id             = db.Column(db.Integer, primary_key=True)

    # unique=True enforces no duplicate usernames at the database level
    username       = db.Column(db.String(80), unique=True, nullable=False)
    email          = db.Column(db.String(120), unique=True, nullable=False)
    _password_hash = db.Column(db.String, nullable=False)

    # One user can own many notes. Deleting a user removes all their notes.
    notes = db.relationship(
        'Note',
        back_populates='user',
        cascade='all, delete-orphan'
    )

    # ── Validators ────────────────────────────────────────────────────────────

    @validates('username')
    def validate_username(self, key, username):
        """Ensure username is not empty."""
        if not username or not username.strip():
            raise ValueError("Username cannot be empty.")
        return username.strip()

    @validates('email')
    def validate_email(self, key, email):
        """Ensure email is not empty and contains an @ symbol."""
        if not email or '@' not in email:
            raise ValueError("A valid email address is required.")
        return email.strip()

    # ── Password handling ─────────────────────────────────────────────────────

    @hybrid_property
    def password_hash(self):
        """
        Block direct access to the password hash.
        Raising an exception here ensures the hash is never accidentally
        serialised or logged.
        """
        raise Exception("Password hashes may not be viewed.")

    @password_hash.setter
    def password_hash(self, password):
        """
        Hash a plain-text password using bcrypt and store the result.
        The original password is never persisted.
        """
        hashed = bcrypt.generate_password_hash(password.encode('utf-8'))
        self._password_hash = hashed.decode('utf-8')

    def authenticate(self, password):
        """
        Return True if the given plain-text password matches the stored hash.
        Used during login to verify credentials.
        """
        return bcrypt.check_password_hash(
            self._password_hash,
            password.encode('utf-8')
        )

    def __repr__(self):
        return f'<User id={self.id} username={self.username!r}>'


# ── Note model ────────────────────────────────────────────────────────────────

class Note(db.Model):
    __tablename__ = 'notes'

    id         = db.Column(db.Integer, primary_key=True)
    title      = db.Column(db.String(200), nullable=False)
    content    = db.Column(db.Text, nullable=False)

    # Automatically set on creation; automatically updated on every change
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,
                           onupdate=datetime.utcnow)

    # Foreign key linking this note to its owner
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False
    )

    # Back-reference to the owning User instance
    user = db.relationship('User', back_populates='notes')

    # ── Validators ────────────────────────────────────────────────────────────

    @validates('title')
    def validate_title(self, key, title):
        """Ensure title is not empty."""
        if not title or not title.strip():
            raise ValueError("Title cannot be empty.")
        return title.strip()

    @validates('content')
    def validate_content(self, key, content):
        """Ensure content is not empty."""
        if not content or not content.strip():
            raise ValueError("Content cannot be empty.")
        return content.strip()

    def __repr__(self):
        return f'<Note id={self.id} title={self.title!r} user_id={self.user_id}>'


# ── Marshmallow schemas ───────────────────────────────────────────────────────

class UserSchema(Schema):
    """
    Serialises a User object to JSON.
    The password hash is intentionally excluded from all output.
    """
    id       = fields.Int(dump_only=True)
    username = fields.Str()
    email    = fields.Str()


class NoteSchema(Schema):
    """Serialises a Note object to JSON, including timestamps."""
    id         = fields.Int(dump_only=True)
    title      = fields.Str()
    content    = fields.Str()
    user_id    = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)