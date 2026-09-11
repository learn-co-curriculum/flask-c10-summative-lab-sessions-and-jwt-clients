from server import ma
from server.models.user import User


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        include_fk = True

    id = ma.auto_field(dump_only=True)
    username = ma.auto_field(required=True)
    email = ma.auto_field(required=True)
    # password_hash is intentionally excluded so it never gets serialized out


user_schema = UserSchema()
users_schema = UserSchema(many=True)
