from flask_sqlalchemy import SQLAlchemy

# Initialize the database
db = SQLAlchemy()

class User(db.Model):
    """User model for storing user information"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    _password_hash = db.Column(db.String)

    # Relationship to notes
    notes = db.relationship('Note', backref='user', lazy=True)

    @property
    def password_hash(self):
        # Don't allow reading the password
        raise AttributeError('password_hash is not a readable attribute')

    @password_hash.setter
    def password_hash(self, password):
        # Hash the password using bcrypt
        from flask_bcrypt import generate_password_hash
        self._password_hash = generate_password_hash(password).decode('utf-8')

    def __repr__(self):
        return f'<User {self.username}>'

class Note(db.Model):
    """Note model for storing user notes"""
    __tablename__ = 'notes'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f'<Note {self.title}>'