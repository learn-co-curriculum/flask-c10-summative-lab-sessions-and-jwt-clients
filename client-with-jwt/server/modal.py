from config import db, bcrypt
from sqlalchemy.ext.hybrid import hybrid_property

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    _password_hash = db.Column(db.String, nullable=False)
    tasks = db.relationship('Task', backref='user', lazy=True, cascade="all, delete-orphan")