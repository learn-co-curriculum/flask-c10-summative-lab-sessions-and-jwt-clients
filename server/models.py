
from sqlalchemy.orm import validates
from app import db, bcrypt

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    tasks = db.relationship("Task", back_populates="user", cascade="all, delete-orphan")

    @validates("username")
    def validate_username(self, key, username):
        if not username:
            raise ValueError("Username is required.")

        username = username.strip()
        if len(username) < 3:
            raise ValueError("Username must be at least 3 characters.")
        return username

    @property
    def password(self):
        raise AttributeError("Password is not readable.")
    
    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def authenticate(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)


class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    completed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    user = db.relationship("User", back_populates="tasks")

    @validates("title")
    def validate_title(self, key, value):
        if not value:
            raise ValueError("Title is required")
        value = value.strip()

        if len(value) < 3:
            raise ValueError("Title must be at least 3 characters.")
        return value