"""
Note and Tag models.

``Note`` is the primary resource of this application.  Each note belongs to
exactly one user and may optionally carry a ``Tag`` label.

``Tag`` is the *additional resource*.  It has two
custom fields beyond the foreign key: ``name`` and ``color``.
"""
from datetime import datetime

from app.extensions import db


class Note(db.Model):
    """A user-owned text note.

    Custom fields (beyond the foreign key)
    ---------------------------------------
    * ``title``   — short heading for the note (required, ≤ 255 chars)
    * ``content`` — body text of the note (required)
    * ``pinned``  — boolean flag; pinned notes appear first in listings
    * ``tag_id``  — optional FK to a Tag for categorisation
    """

    __tablename__ = "notes"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False, index=True
    )
    tag_id = db.Column(
        db.Integer, db.ForeignKey("tags.id"), nullable=True, index=True
    )
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    # Extra custom field 1: pinned status
    pinned = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    author = db.relationship("User", back_populates="notes")
    tag = db.relationship("Tag", back_populates="notes")

    # ------------------------------------------------------------------ #
    # Helpers                                                              #
    # ------------------------------------------------------------------ #

    @staticmethod
    def owned_by(note_id: int, user_id: int) -> "Note | None":
        """Return the note if it exists *and* belongs to *user_id*."""
        return Note.query.filter_by(id=note_id, user_id=user_id).first()

    def to_dict(self) -> dict:
        """Return a JSON-serialisable representation of the note."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "tag_id": self.tag_id,
            "title": self.title,
            "content": self.content,
            "pinned": self.pinned,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    def __repr__(self) -> str:
        return f"<Note {self.id!r}: {self.title!r}>"


class Tag(db.Model):
    """A user-defined label that can be applied to notes.

    """

    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False, index=True
    )
    # Custom field 1: tag name
    name = db.Column(db.String(80), nullable=False)
    # Custom field 2: display colour
    color = db.Column(db.String(7), nullable=False, default="#3B82F6")
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    author = db.relationship("User", back_populates="tags")
    notes = db.relationship("Note", back_populates="tag", lazy="dynamic")

    __table_args__ = (
        # A user cannot have two tags with the same name
        db.UniqueConstraint("user_id", "name", name="uq_tag_user_name"),
    )

    def to_dict(self) -> dict:
        """Return a JSON-serialisable representation of the tag."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "color": self.color,
            "created_at": self.created_at.isoformat(),
        }

    def __repr__(self) -> str:
        return f"<Tag {self.name!r}>"
