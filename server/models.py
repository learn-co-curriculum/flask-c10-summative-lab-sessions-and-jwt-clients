from config import db, bcrypt
from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    _password_hash = db.Column(db.String(255), nullable=False)

    notes = db.relationship(
        "Note",
        backref="user",
        cascade="all, delete-orphan"
    )

    @hybrid_property
    def password_hash(self):
        return self._password_hash

    @password_hash.setter
    def password_hash(self, password):
        if not password:
            raise ValueError("Password cannot be empty")

        hashed = bcrypt.generate_password_hash(password.encode("utf-8"))
        self._password_hash = hashed.decode("utf-8")

    def authenticate(self, password):
        return bcrypt.check_password_hash(
            self._password_hash,
            password.encode("utf-8")
        )

    @validates("username")
    def validate_username(self, key, username):
        if not username or username.strip() == "":
            raise ValueError("Username cannot be empty")
        return username.strip()


class Note(db.Model):
    __tablename__ = "notes"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(80), nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    @validates("title", "content", "category")
    def validate_fields(self, key, value):
        if value is None:
            return value

        if isinstance(value, str) and value.strip() == "":
            raise ValueError(f"{key} cannot be empty")

        return value.strip() if isinstance(value, str) else value