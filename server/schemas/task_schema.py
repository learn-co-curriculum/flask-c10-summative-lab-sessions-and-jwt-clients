from marshmallow import Schema, fields


class TaskSchema(Schema):
    """Schema for serializing task data."""

    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    description = fields.Str()
    due_date = fields.Date(allow_none=True)
    completed = fields.Bool()
    user_id = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    