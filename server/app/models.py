from sqlalchemy.ext.hybrid import hybrid_property
from marshmallow import fields, validate
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from app import db, bcrypt

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String)
    _password_hash = db.Column(db.String)

    notes = db.relationship('Note', back_populates='user', cascade="all, delete-orphan")

    @hybrid_property
    def password_hash(self):
        raise AttributeError("Password hashes may not be viewed")
    
    @password_hash.setter
    def password_hash(self, password):
        password_hash = bcrypt.generate_password_hash(password.encode('utf-8'))
        self._password_hash = password_hash.decode('utf-8')

    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password.encode('utf-8'))
    
    def __repr__(self):
        return f'<User: {self.username}>'
    
class Note(db.Model):
    __tablename__ = 'notes'


    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    body = db.Column(db.String(200))
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))

    user = db.relationship('User', back_populates='notes')

    def __repr__(self):
        return f'<Note  {self.title} : {self.body}>'
    

# schemas
class UserSchema(SQLAlchemyAutoSchema):
    id = fields.Int(dump_only=True)
    username = fields.String(required=True)

    notes = fields.List(fields.Nested(lambda: NoteSchema(exclude=("user",))), dump_only=True)
    class Meta:
        model = User
        fields = ("id", "username", "notes")
        load_instance=True
        sqla_session = db.session
        ordered=True

class NoteSchema(SQLAlchemyAutoSchema):
    id = fields.Int(dump_only=True)
    title = fields.String(required=True)
    body = fields.String(validate=validate.Length(max=200))
    user_id = fields.Int(required=True)

    user = fields.Nested(lambda: UserSchema(exclude=("notes",)), dump_only=True)

    class Meta:
        model = Note
        fields = ("id", "title", "body", "user_id", "user")
        load_instance=True
        sqla_session = db.session
        ordered=True


user_schema = UserSchema()
users_schema = UserSchema(many=True)

note_schema = NoteSchema()
notes_schema = NoteSchema(many=True)