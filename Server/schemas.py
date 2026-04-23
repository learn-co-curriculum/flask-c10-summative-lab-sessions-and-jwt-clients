from marshmallow import Schema, fields, validate

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=validate.Length(min=1, error = "Username can't be empty."))
    email = fields.Email(required=True, error_messages={"required": "Email is required."})
    password = fields.Str(required=True, load_only=True, validate=validate.Length(min=6))
    
class ExpenseSchema(Schema):
    id = fields.Int(dump_only = True)
    title = fields.Str(required = True, validate=validate.Length(min=1, error = "Title can't be empty."))
    amount = fields.Float(required = True, validate=validate.Range(min=0.01, error = "Amount must be a positive number."))
    category = fields.Str(required = True, validate=validate.OneOf(['food', 'transport', 'entertainment', 'utilities', 'health', 'other'], error = "That isn't a valid category."))
    user_id = fields.Int(dump_only = True)
    

user_schema = UserSchema()
users_schema = UserSchema(many=True)
expense_schema = ExpenseSchema()
expenses_schema = ExpenseSchema(many=True)   