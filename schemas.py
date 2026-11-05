"""Marshmallow schemas: validate incoming JSON and serialize model objects."""
from marshmallow import EXCLUDE, Schema, ValidationError, fields, validate


def not_blank(value):
    if not value.strip():
        raise ValidationError("Cannot be blank.")


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str()
    # The password hash is intentionally not a field, so it is never returned.


class NoteSchema(Schema):
    class Meta:
        # Ignore unknown keys (e.g. a client trying to send someone else's user_id).
        unknown = EXCLUDE

    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=[not_blank, validate.Length(max=100)])
    content = fields.Str(required=True, validate=not_blank)
    category = fields.Str(load_default="general", validate=validate.Length(min=1, max=50))
    is_pinned = fields.Bool(load_default=False)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    user_id = fields.Int(dump_only=True)


user_schema = UserSchema()
note_schema = NoteSchema()
notes_schema = NoteSchema(many=True)