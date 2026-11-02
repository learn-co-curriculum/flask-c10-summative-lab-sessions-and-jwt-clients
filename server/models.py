from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import validates

from config import bcrypt, db

MOOD_CHOICES = ["happy", "calm", "excited", "neutral", "tired", "sad", "anxious", "angry"]


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    _password_hash = db.Column(db.String, nullable=False)

    @hybrid_property
    def password_hash(self):
        raise AttributeError("Password hashes may not be viewed.")

    @password_hash.setter
    def password_hash(self, password):
        if not password or len(password) < 6:
            raise ValueError("Password must be at least 6 characters.")
        self._password_hash = bcrypt.generate_password_hash(password.encode("utf-8")).decode("utf-8")

    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password.encode("utf-8"))

    @validates("username")
    def validate_username(self, key, username):
        username = (username or "").strip()
        if not 3 <= len(username) <= 50:
            raise ValueError("Username must be between 3 and 50 characters.")
        return username


class Mood(db.Model):
    __tablename__ = "moods"

    id = db.Column(db.Integer, primary_key=True)
    mood = db.Column(db.String(20), nullable=False)
    intensity = db.Column(db.Integer, nullable=False)
    note = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    user = db.relationship("User", backref=db.backref("moods", cascade="all, delete-orphan"))

    @validates("mood")
    def validate_mood(self, key, mood):
        mood = (mood or "").strip().lower() if isinstance(mood, str) else ""
        if mood not in MOOD_CHOICES:
            raise ValueError(f"Mood must be one of: {', '.join(MOOD_CHOICES)}.")
        return mood

    @validates("intensity")
    def validate_intensity(self, key, intensity):
        if isinstance(intensity, bool) or not isinstance(intensity, int) or not 1 <= intensity <= 10:
            raise ValueError("Intensity must be a whole number from 1 to 10.")
        return intensity

    @validates("note")
    def validate_note(self, key, note):
        if note is not None and len(note) > 500:
            raise ValueError("Note must be 500 characters or fewer.")
        return note


# Join table linking moods and activities (many-to-many).
mood_activities = db.Table(
    "mood_activities",
    db.Column("mood_id", db.Integer, db.ForeignKey("moods.id"), primary_key=True),
    db.Column("activity_id", db.Integer, db.ForeignKey("activities.id"), primary_key=True),
)


class Activity(db.Model):
    __tablename__ = "activities"
    __table_args__ = (db.UniqueConstraint("user_id", "name"),)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    user = db.relationship("User", backref=db.backref("activities", cascade="all, delete-orphan"))
    moods = db.relationship("Mood", secondary=mood_activities, backref="activities")

    @validates("name")
    def validate_name(self, key, name):
        name = (name or "").strip() if isinstance(name, str) else ""
        if not 1 <= len(name) <= 50:
            raise ValueError("Activity name must be between 1 and 50 characters.")
        return name


class Journal(db.Model):
    __tablename__ = "journals"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    user = db.relationship("User", backref=db.backref("journals", cascade="all, delete-orphan"))

    @validates("title")
    def validate_title(self, key, title):
        title = (title or "").strip() if isinstance(title, str) else ""
        if not 1 <= len(title) <= 100:
            raise ValueError("Title must be between 1 and 100 characters.")
        return title

    @validates("content")
    def validate_content(self, key, content):
        content = (content or "").strip() if isinstance(content, str) else ""
        if not content:
            raise ValueError("Content cannot be empty.")
        return content