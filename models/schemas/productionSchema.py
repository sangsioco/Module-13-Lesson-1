from marshmallow import fields, validate
from schema import ma

class ProductionSchema(ma.Schema):
    id = fields.Int(dump_only=True)  
    product_id = fields.Int(required=True)  
    quantity_produced = fields.Int(required=True, validate=validate.Range(min=1))  
    date_produced = fields.Date(required=True) 

production_schema = ProductionSchema()
productions_schema = ProductionSchema(many=True)

