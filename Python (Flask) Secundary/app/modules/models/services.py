from typing import Any, Dict, List, Tuple
from sqlalchemy.orm import joinedload
from werkzeug.exceptions import NotFound
from .models import Model
from ..brands.models import Brand
from .schemas import ModelCreateSchema, ModelUpdateSchema
from ...extensions import db

def _serialize_model(m: Model) -> Dict[str, Any]:
    return {
        "id": m.id,
        "marca_id": m.brand_id,
        "nome": m.nome,
        "fipeValue": float(m.fipeValue),
        "brand": {"id": m.brand.id, "name": m.brand.name},
    }

def create_model(payload: dict) -> Dict[str, Any]:
    data = ModelCreateSchema().load(payload)
    brand = Brand.query.get(data["marca_id"]) # type: ignore
    if not brand:
        raise NotFound("Marca inválida")

    m = Model(brand_id=brand.id, nome=data["nome"], fipeValue=data["fipeValue"]) # type: ignore
    db.session.add(m)
    db.session.commit()

    m = Model.query.options(joinedload(Model.brand)).get(m.id)  # type: ignore
    return _serialize_model(m) # type: ignore

def list_models(page: int, limit: int, search: str | None) -> Tuple[int, List[Dict[str, Any]]]:
    q = Model.query.join(Brand).options(joinedload(Model.brand))

    if search:
        q = q.filter(Model.nome.ilike(f"%{search}%"))

    total = q.count()
    items = (
        q.order_by(Model.nome.asc())
         .offset((page - 1) * limit)
         .limit(limit)
         .all()
    )
    return total, [_serialize_model(m) for m in items]

def get_model(id: int) -> Dict[str, Any]:
    m = (
        Model.query.options(joinedload(Model.brand))
        .get(id)
    )
    if not m:
        raise NotFound("Modelo não encontrado")
    return _serialize_model(m)

def update_model(id: int, payload: dict) -> Dict[str, Any]:
    data = ModelUpdateSchema().load(payload, partial=True)

    m = Model.query.get(id)
    if not m:
        raise NotFound("Modelo não encontrado")

    if "marca_id" in data and data["marca_id"] != m.brand_id: # type: ignore
        brand = Brand.query.get(data["marca_id"]) # type: ignore
        if not brand:
            raise NotFound("Marca inválida")
        m.brand_id = brand.id

    if "nome" in data: # type: ignore
        m.nome = data["nome"] # type: ignore

    if "fipeValue" in data: # type: ignore
        m.fipeValue = data["fipeValue"] # type: ignore

    db.session.commit()

    m = Model.query.options(joinedload(Model.brand)).get(m.id)  # type: ignore
    return _serialize_model(m) # type: ignore

def remove_model(id: int) -> None:
    m = Model.query.get(id)
    if not m:
        raise NotFound("Modelo não encontrado")
    db.session.delete(m)
    db.session.commit()
