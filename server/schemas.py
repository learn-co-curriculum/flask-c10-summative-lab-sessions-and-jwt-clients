from marshmallow import Schema, fields, validate


class UserSchema(Schema):
    id = fields.Int(dump_only=True)

    username = fields.Str(
        required=True,
        validate=validate.Length(min=3, max=80)
    )

    created_at = fields.DateTime(dump_only=True)


class NoteSchema(Schema):
    id = fields.Int(dump_only=True)

    title = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=200)
    )

    content = fields.Str(
        required=True,
        validate=validate.Length(min=1)
    )

    category = fields.Str(load_default="General")

    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    user_id = fields.Int(dump_only=True)


user_schema = UserSchema()
users_schema = UserSchema(many=True)

note_schema = NoteSchema()
notes_schema = NoteSchema(many=True)
