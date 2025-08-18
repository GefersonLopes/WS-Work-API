from .models import Brand
from .schemas import BrandCreateSchema, BrandUpdateSchema
from ...extensions import db
from werkzeug.exceptions import NotFound

def _serialize(b: Brand) -> dict:
    return {"id": b.id, "nome_marca": b.name}

def create(payload: dict) -> dict:
    data = BrandCreateSchema().load(payload)
    b = Brand(name=data["nome_marca"]) # type: ignore
    db.session.add(b)
    db.session.commit()
    return _serialize(b)

def list_all() -> list[dict]:
    items = Brand.query.order_by(Brand.name.asc()).all()
    return [_serialize(b) for b in items]

def find_one(id: int) -> dict:
    b = Brand.query.get(id)
    if not b:
        raise NotFound("Marca não encontrada")
    return _serialize(b)

def update(id: int, payload: dict) -> dict:
    data = BrandUpdateSchema().load(payload)
    b = Brand.query.get(id)
    if not b:
        raise NotFound("Marca não encontrada")
    b.name = data["nome_marca"] # type: ignore
    db.session.commit()
    return _serialize(b)

def remove(id: int) -> None:
    b = Brand.query.get(id)
    if not b:
        raise NotFound("Marca não encontrada")
    db.session.delete(b)
    db.session.commit()
