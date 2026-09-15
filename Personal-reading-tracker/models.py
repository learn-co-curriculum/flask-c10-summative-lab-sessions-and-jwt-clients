from import SQLAlchemy  # type: ignore[import-not-found]
 
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
 
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
 
    reading_entries = db.relationship(
        'ReadingEntry',
        back_populates='user',
        cascade='all, delete-orphan'
    )
    def __repr__(self):
        return f'<User {self.username!r}>'

class ReadingEntry(db.Model):
    __tablename__ = 'reading_entries'
 
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    status = db.Column(db.String, nullable=False, default='want_to_read')
    rating = db.Column(db.Integer, nullable=True)
    start_date = db.Column(db.Date, nullable=True)
    completion_date = db.Column(db.Date, nullable=True)
 
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', back_populates='reading_entries')
 
    def __repr__(self):
        return f'<ReadingEntry {self.title!r} by {self.author!r}>'