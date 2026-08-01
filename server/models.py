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
    _password_hash = db.Column(db.String, nullable=False)

    # One user owns many notes. Deleting the user removes all their notes.
    notes = db.relationship(
        'Note',
        back_populates='user',
        cascade='all, delete-orphan'
    )

    # ── Validators ────────────────────────────────────────────────────────────

    @validates('username')
    def validate_username(self, key, username):
        """Ensure username is not blank before saving."""
        if not username or not username.strip():
            raise ValueError("Username cannot be empty.")
        return username.strip()

    # ── Password handling ─────────────────────────────────────────────────────

    @hybrid_property
    def password_hash(self):
        raise Exception("Password hashes may not be viewed.")

    @password_hash.setter
    def password_hash(self, password):
        hashed = bcrypt.generate_password_hash(password.encode('utf-8'))
        self._password_hash = hashed.decode('utf-8')

    def authenticate(self, password):
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

    # NEW — optional category field with a default value
    category   = db.Column(db.String(50), nullable=False, default='General')

    # NEW — pinned notes sort to the top of the list
    is_pinned  = db.Column(db.Boolean, nullable=False, default=False)


    # Automatically set on creation; updated on every change
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,
                           onupdate=datetime.utcnow)

    # Foreign key — every note belongs to exactly one user
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False
    )

    # Back-reference to the owning User
    user = db.relationship('User', back_populates='notes')

    @validates('title')
    def validate_title(self, key, title):
        """Ensure title is not blank before saving."""
        if not title or not title.strip():
            raise ValueError("Title cannot be empty.")
        return title.strip()

    @validates('content')
    def validate_content(self, key, content):
        """Ensure content is not blank before saving."""
        if not content or not content.strip():
            raise ValueError("Content cannot be empty.")
        return content.strip()

    def __repr__(self):
        return f'<Note id={self.id} title={self.title!r} user_id={self.user_id}>'


# ── Marshmallow schemas ───────────────────────────────────────────────────────

class UserSchema(Schema):
    """
    Serialises a User to JSON.
    """
    id       = fields.Int(dump_only=True)
    username = fields.Str()


class NoteSchema(Schema):
    """Serialises a Note to JSON, including timestamps and owner id."""
    id         = fields.Int(dump_only=True)
    title      = fields.Str()
    content    = fields.Str()
    category   = fields.Str()
    is_pinned  = fields.Bool()
    user_id    = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)