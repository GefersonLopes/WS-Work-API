from marshmallow import Schema, fields, validate

class BrandCreateSchema(Schema):
    nome_marca = fields.Str(required=True, validate=[validate.Length(min=1, max=120)])

class BrandUpdateSchema(BrandCreateSchema):
    pass
