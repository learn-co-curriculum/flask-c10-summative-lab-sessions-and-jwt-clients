from marshmallow import Schema, fields, validates, ValidationError

class UserSignupSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    password_confirmation = fields.Str(required=True)

    @validates("password_confirmation")
    def validate_password_match(self, value, **kwargs):
        if self.context.get("password") != value:
            raise ValidationError("Password confirmation does not match password.")

class UserLoginSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)

class NoteCreateSchema(Schema):
    title = fields.Str(required=True)
    content = fields.Str(required=True)
    mood = fields.Str(required=False)

class NoteUpdateSchema(Schema):
    title = fields.Str(required=False)
    content = fields.Str(required=False)
    mood = fields.Str(required=False)
