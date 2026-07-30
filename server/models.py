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