from marshmallow import Schema, fields, validate

#create Expense schema
class ExpenseSchema(Schema):
    title = fields.String(required=True, validate=validate.Length(min=1))
    amount = fields.Float(required=True)
    category = fields.String(required=False)
    description = fields.String(required=False)