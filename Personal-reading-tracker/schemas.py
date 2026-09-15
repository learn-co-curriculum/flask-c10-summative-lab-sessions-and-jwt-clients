from flask_marshmallow import Marshmallow
from marshmallow import fields, validate

ma = Marshmallow()


class UserSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = (
            "id",
            "username",
            "email",
            "password",
            "created_at",
            "updated_at",
        )

    id = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=validate.Length(min=3, max=80))
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True, validate=validate.Length(min=6))
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class BookSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = (
            "id",
            "title",
            "author",
            "genre",
            "status",
            "pages",
            "current_page",
            "notes",
            "user_id",
            "created_at",
            "updated_at",
        )

    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    author = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    genre = fields.Str(load_default=None, allow_none=True)
    status = fields.Str(required=True, validate=validate.OneOf(["want_to_read", "reading", "finished"]))
    pages = fields.Int(required=True, validate=validate.Range(min=1))
    current_page = fields.Int(load_default=0, validate=validate.Range(min=0))
    notes = fields.Str(load_default="", allow_none=True)
    user_id = fields.Int(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class ReadingSessionSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = (
            "id",
            "book_id",
            "date",
            "minutes_read",
            "pages_read",
            "notes",
            "created_at",
        )

    id = fields.Int(dump_only=True)
    book_id = fields.Int(required=True)
    date = fields.Date(required=True)
    minutes_read = fields.Int(required=True, validate=validate.Range(min=1))
    pages_read = fields.Int(required=True, validate=validate.Range(min=0))
    notes = fields.Str(load_default="", allow_none=True)
    created_at = fields.DateTime(dump_only=True)


user_schema = UserSchema()
users_schema = UserSchema(many=True)

book_schema = BookSchema()
books_schema = BookSchema(many=True)

reading_session_schema = ReadingSessionSchema()
reading_sessions_schema = ReadingSessionSchema(many=True)
