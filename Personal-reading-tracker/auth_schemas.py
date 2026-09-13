from marshmallow import Schema, ValidationError, fields, validate, validates, validates_schema


class LoginSchema(Schema):
    username = fields.String(required=True, validate=validate.Length(min=1, max=80))
    password = fields.String(required=True, load_only=True, validate=validate.Length(min=1))

    @validates('password')
    def validate_password_bytes(self, value):
        if len(value.encode('utf-8')) > 72:
            raise ValidationError('Password must be at most 72 UTF-8 bytes.')


class RegistrationSchema(LoginSchema):
    username = fields.String(required=True, validate=validate.Regexp(r'^[A-Za-z0-9_-]{3,80}$'))
    email = fields.Email(required=True, validate=validate.Length(max=254))
    password = fields.String(required=True, load_only=True, validate=validate.Length(min=8))
    password_confirmation = fields.String(load_only=True)

    @validates_schema
    def check_confirmation(self, data, **kwargs):
        if 'password_confirmation' in data and data['password_confirmation'] != data['password']:
            raise ValidationError('Passwords must match.', field_name='password_confirmation')


class PublicUserSchema(Schema):
    id = fields.Integer(dump_only=True)
    username = fields.String(dump_only=True)
    email = fields.Email(dump_only=True)
