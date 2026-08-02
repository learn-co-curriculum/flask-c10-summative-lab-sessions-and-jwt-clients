from .user_schema import UserSchema
from .task_schema import TaskSchema

user_schema = UserSchema()
users_schema = UserSchema(many=True)
task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)