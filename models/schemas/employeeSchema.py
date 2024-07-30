from marshmallow import Schema, fields, validate

class EmployeeSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1))
    position = fields.Str(required=True, validate=validate.Length(min=1))

employee_schema = EmployeeSchema()
employees_schema = EmployeeSchema(many=True)
