"""
User model.

Stores authentication credentials.  Passwords are never stored in plain text;
bcrypt is used to hash them before persistence.  JWT tokens are generated and
verified directly on the model to keep auth logic co-located with the entity
it describes.
"""

from datetime import datetime, timedelta
from typing import Union

import jwt
from flask import current_app

from app.extensions import db, bcrypt


class User(db.Model):
    """Represents an authenticated application user.

    Constraints
    -----------
    * ``username`` is unique and indexed for fast look-ups.
    * ``password_hash`` is never exposed in serialised output.
    """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    # One-to-many: a user owns many notes
    notes = db.relationship(
        "Note", back_populates="author", lazy="dynamic", cascade="all, delete-orphan"
    )
    # One-to-many: a user can create many tags
    tags = db.relationship(
        "Tag", back_populates="author", lazy="dynamic", cascade="all, delete-orphan"
    )

    # ------------------------------------------------------------------ #
    # Password helpers                                                     #
    # ------------------------------------------------------------------ #

    def set_password(self, plaintext: str) -> None:
        """Hash *plaintext* with bcrypt and store the result."""
        self.password_hash = bcrypt.generate_password_hash(plaintext).decode("utf-8")

    def check_password(self, plaintext: str) -> bool:
        """Return *True* if *plaintext* matches the stored hash."""
        return bcrypt.check_password_hash(self.password_hash, plaintext)

    # ------------------------------------------------------------------ #
    # JWT helpers                                                          #
    # ------------------------------------------------------------------ #

    def generate_token(self) -> str:
        """Encode a signed JWT containing the user's identity.

        The token expires after the duration defined in
        ``JWT_EXPIRATION_DELTA`` (default 24 hours).
        """
        payload = {
            "user_id": self.id,
            "username": self.username,
            "exp": datetime.utcnow() + current_app.config["JWT_EXPIRATION_DELTA"],
        }
        return jwt.encode(
            payload,
            current_app.config["JWT_SECRET_KEY"],
            algorithm="HS256",
        )

    @staticmethod
    def verify_token(token: str) -> Union[dict, None]:
        """Decode and validate *token*.

        Returns the payload dict on success, or *None* if the token is
        expired or otherwise invalid.
        """
        try:
            return jwt.decode(
                token,
                current_app.config["JWT_SECRET_KEY"],
                algorithms=["HS256"],
            )
        except (jwt.InvalidTokenError, jwt.ExpiredSignatureError):
            return None

    # ------------------------------------------------------------------ #
    # Serialisation                                                        #
    # ------------------------------------------------------------------ #

    def to_dict(self) -> dict:
        """Return a safe, JSON-serialisable representation.

        The password hash is intentionally excluded.
        """
        return {
            "id": self.id,
            "username": self.username,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    def __repr__(self) -> str:
        return f"<User {self.username!r}>"
