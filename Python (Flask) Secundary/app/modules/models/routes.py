from flask import Blueprint, request, jsonify
from .models import Model
from ..brands.models import Brand
from .schemas import ModelCreateSchema, ModelUpdateSchema
from ...extensions import db
from ...common.dto import get_pagination_defaults

bp = Blueprint("models", __name__)

@bp.post("/")
def create():
    data = ModelCreateSchema().load(request.get_json() or {})
    brand = Brand.query.get(data["marca_id"]) # type: ignore
    if not brand:
        return jsonify({"message": "Marca inválida"}), 404
    m = Model(brand_id=brand.id, nome=data["nome"], fipeValue=data["fipeValue"]) # type: ignore
    db.session.add(m); db.session.commit()
    return jsonify({"id": m.id, "marca_id": m.brand_id, "nome": m.nome, "fipeValue": float(m.fipeValue)}), 201

@bp.get("/")
def list_all():
    page, limit, search = get_pagination_defaults()
    q = Model.query.join(Brand).options(db.joinedload(Model.brand))
    if search:
        q = q.filter(Model.nome.ilike(f"%{search}%"))
    total = q.count()
    items = q.order_by(Model.nome.asc()).offset((page-1)*limit).limit(limit).all()
    return jsonify({
        "total": total, "page": page, "limit": limit,
        "items": [
            {"id": m.id, "marca_id": m.brand_id, "nome": m.nome, "fipeValue": float(m.fipeValue), "brand": m.brand.name}
            for m in items
        ]
    })

@bp.get("/public/cars.json")
def list_for_frontend():
    models = Model.query.join(Brand).options(db.joinedload(Model.brand)).order_by(Model.nome.asc()).all()
    return jsonify([
        {"id": m.id, "name": m.nome, "brand": m.brand.name, "valor_fipe": float(m.fipeValue)}
        for m in models
    ])

@bp.get("/<int:id>")
def find_one(id: int):
    m = Model.query.options(db.joinedload(Model.brand)).get_or_404(id, description="Modelo não encontrado")
    return jsonify({"id": m.id, "marca_id": m.brand_id, "nome": m.nome, "fipeValue": float(m.fipeValue)})

@bp.patch("/<int:id>")
def update(id: int):
    data = ModelUpdateSchema().load(request.get_json() or {}, partial=True)
    m = Model.query.get_or_404(id, description="Modelo não encontrado")

    if "marca_id" in data and data["marca_id"] != m.brand_id: # type: ignore
        brand = Brand.query.get(data["marca_id"])   # type: ignore
        if not brand:
            return jsonify({"message":"Marca inválida"}), 404
        m.brand_id = brand.id
    
    if "nome" in data: m.nome = data["nome"] # type: ignore
    
    if "fipeValue" in data: m.fipeValue = data["fipeValue"] # type: ignore
    
    db.session.commit()
    return jsonify({"id": m.id, "marca_id": m.brand_id, "nome": m.nome, "fipeValue": float(m.fipeValue)})

@bp.delete("/<int:id>")
def remove(id: int):
    m = Model.query.get_or_404(id, description="Modelo não encontrado")
    db.session.delete(m); db.session.commit()
    return "", 204
