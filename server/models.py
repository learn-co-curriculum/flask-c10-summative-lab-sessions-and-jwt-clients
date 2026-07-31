from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import validates
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields
from app import bcrypt
db = SQLAlchemy()

class User(db.Model):
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String, unique=True)
  _password_hash = db.Column(db.String, nullable=False)
  notes = db.relationship('Note', back_populates='user')

  def __repr__(self):
    return f"User {self.id}, {self.username}"
  
  @hybrid_property
  def password_hash(self):
    # What happens when someone tries to access the hashed password using self.password_hash it can still be viewed if you put an underscore before the word password
    raise Exception("Hashes passwords cannot be viewed!")

  @password_hash.setter
  def password_hash(self, password):
    # Encode -> human-readable string to bytes
    # Decode -> bytes to human-readable string
    # Encrypts the code the user inputs
    password_hash = bcrypt.generate_password_hash(password.encode('utf-8'))
    # Sets the encrypted password to the password instance
    self._password_hash = password_hash.decode('utf-8')

  def authenticate(self, password):
    # Checks the hashed password in the database against the password sent by the user
    return bcrypt.check_password_hash(self._password_hash, password.encode('utf-8'))


class Note(db.Model):
  __tablename__ = 'notes'
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String, nullable=False)
  content = db.Column(db.String)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  user = db.relationship('User', back_populates='notes')

class UserSchema(Schema):
  username = fields.String(required=True, error_messages={"required": "Username is required."})
  _password_hash = fields.String(required=True, error_messages={"required": "Password is required."})
  notes = fields.Nested(lambda: NoteSchema(exclude=('user', )))

class NoteSchema(Schema):
  title = fields.String()
  content = fields.String()
  user = fields.Nested(lambda: UserSchema(exclude=('notes', )))