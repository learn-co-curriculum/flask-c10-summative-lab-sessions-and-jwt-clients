from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import validates
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    _password_hash = db.Column(db.String)

   
    notes = db.relationship('Note', back_populates='user')

   
    @hybrid_property
    def password_hash(self):
        raise AttributeError('Password hashes may not be viewed.')

   
    @password_hash.setter
    def password_hash(self, password):
        password_hash = bcrypt.generate_password_hash(password.encode('utf-8'))
        self._password_hash = password_hash.decode('utf-8')

    
    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password.encode('utf-8'))

    def __repr__(self):
        return f'<User {self.id}, {self.username}>'


class Note(db.Model):
    __tablename__ = 'notes'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.Text)
    category = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

   
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

   
    user = db.relationship('User', back_populates='notes')

    def __repr__(self):
        return f'<Note {self.id}, {self.title}>'    