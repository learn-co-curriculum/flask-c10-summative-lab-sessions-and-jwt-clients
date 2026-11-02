from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str()


class ActivitySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    user_id = fields.Int()


class JournalSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str()
    content = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    user_id = fields.Int()

    class MoodSchema(Schema):
    id = fields.Int(dump_only=True)
    mood = fields.Str()
    intensity = fields.Int()
    note = fields.Str(allow_none=True)
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    user_id = fields.Int()
    activities = fields.List(
        fields.Nested(lambda: ActivitySchema(only=("id", "name")))
    )