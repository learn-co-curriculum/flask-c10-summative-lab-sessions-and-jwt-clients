from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy.orm import validates

# Initialize extensions 
db = SQLAlchemy()
bcrypt = Bcrypt()


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)

    notes = db.relationship(
        "Note",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    def set_password(self, password: str) -> None:
        """Hash and store the user's password securely."""
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password: str) -> bool:
        """Verify a password against the stored password hash."""
        return bcrypt.check_password_hash(self.password_hash, password)


class Note(db.Model):
    """
    A user-owned resource.
    Each note belongs to exactly one user.
    """
    __tablename__ = "notes"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String, nullable=False)
    content = db.Column(db.Text, nullable=False)

    # Ownership (FK)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # Relationship back to the user
    user = db.relationship("User", back_populates="notes")

    @validates("title")
    def validate_title(self, key, value):
  
        if not value or not value.strip():
            raise ValueError("Title is required.")
        return value.strip()

    @validates("content")
    def validate_content(self, key, value):
        # Simple validation: content must not be empty/whitespace
        if not value or not value.strip():
            raise ValueError("Content is required.")
        return value.strip()