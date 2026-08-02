from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)


class TaskSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    description = fields.Str()
    completed = fields.Bool()
    user_id = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


user_schema = UserSchema()
task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)