from marshmallow import Schema, fields, ValidationError, validate
from ...utils import normalize_upper_no_accent

ALLOWED_FUELS = {'GASOLINA','ETANOL','FLEX','DIESEL','HIBRIDO','ELETRICO'}

def fuel_field(value: str):
    norm = normalize_upper_no_accent(value)
    if norm not in ALLOWED_FUELS:
        raise ValidationError(f"combustivel deve ser um de: {', '.join(sorted(ALLOWED_FUELS))}")
    return norm

class CarCreateSchema(Schema):
    modelo_id   = fields.Int(required=True)
    ano         = fields.Int(required=True, validate=[validate.Range(min=1950, max=2100)])
    combustivel = fields.Function(serialize=lambda v: v, deserialize=fuel_field, required=True)
    num_portas  = fields.Int(required=True, validate=[validate.Range(min=2, max=6)])
    cor         = fields.Str(required=True, validate=[validate.Length(min=1, max=40)])

class CarUpdateSchema(Schema):
    modelo_id   = fields.Int(required=False)
    ano         = fields.Int(required=False, validate=[validate.Range(min=1950, max=2100)])
    combustivel = fields.Function(serialize=lambda v: v, deserialize=fuel_field, required=False)
    num_portas  = fields.Int(required=False, validate=[validate.Range(min=2, max=6)])
    cor         = fields.Str(required=False, validate=[validate.Length(min=1, max=40)])
