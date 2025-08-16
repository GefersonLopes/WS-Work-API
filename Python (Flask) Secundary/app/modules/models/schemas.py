from marshmallow import Schema, fields, validate

class ModelCreateSchema(Schema):
    marca_id  = fields.Int(required=True)
    nome      = fields.Str(required=True, validate=validate.Length(min=1, max=120))
    fipeValue = fields.Decimal(required=True, as_string=False, places=2)

class ModelUpdateSchema(ModelCreateSchema):
    pass
