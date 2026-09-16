from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
bcrypt = Bcrypt()


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    notes = db.relationship("Note", back_populates="user", cascade="all, delete-orphan")

    @property
    def password(self):
        raise AttributeError("Password is not readable.")

    @password.setter
    def password(self, password_value):
        self.password_hash = bcrypt.generate_password_hash(password_value).decode("utf-8")

    def check_password(self, password_value):
        return bcrypt.check_password_hash(self.password_hash, password_value)

    def serialize(self):
        return {"id": self.id, "username": self.username}


class Note(db.Model):
    __tablename__ = "notes"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False, default="Notes")
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime,
        server_default=db.func.now(),
        onupdate=db.func.now(),
    )
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("User", back_populates="notes")

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "category": self.category or "Notes",
            "user_id": self.user_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
