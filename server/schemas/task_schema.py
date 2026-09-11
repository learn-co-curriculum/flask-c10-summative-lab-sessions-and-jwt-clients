from server import ma
from server.models.task import Task


class TaskSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Task
        load_instance = True
        include_fk = True

    id = ma.auto_field(dump_only=True)
    title = ma.auto_field(required=True)
    description = ma.auto_field()
    completed = ma.auto_field()
    user_id = ma.auto_field(dump_only=True)


task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)
