from marshmallow import fields
from schema import ma

class EmployeeSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    position = fields.Str(required=True)

# added for for employee performance m13l2 objective 2
class EmployeeProductionSchema(ma.Schema):
    employee_name = fields.String(required=True)
    total_quantity_produced = fields.Integer(required=True)

# added for for employee performance m13l2 objective 2
employee_production_schma = EmployeeProductionSchema()

employee_schema = EmployeeSchema()
employees_schema = EmployeeSchema(many=True)
