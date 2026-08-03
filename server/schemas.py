from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str()

class TaskSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str()
    description = fields.Str()
    completed = fields.Bool()
   


user_schema = UserSchema()
users_schema = UserSchema(many=True)

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)