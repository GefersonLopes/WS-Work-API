from flask import Blueprint, request, jsonify, abort
from .models import Brand
from .schemas import BrandCreateSchema, BrandUpdateSchema
from ...extensions import db

bp = Blueprint("brands", __name__)

@bp.post("/")
def create():
    data = BrandCreateSchema().load(request.get_json() or {})
    b = Brand(name=data["nome_marca"]) # type: ignore
    db.session.add(b)
    db.session.commit()
    return jsonify({"id": b.id, "nome_marca": b.name}), 201

@bp.get("/")
def list_all():
    items = Brand.query.order_by(Brand.name.asc()).all()
    return jsonify([{"id": b.id, "nome_marca": b.name} for b in items])

@bp.get("/<int:id>")
def find_one(id: int):
    b = Brand.query.get_or_404(id, description="Marca não encontrada")
    return jsonify({"id": b.id, "nome_marca": b.name})

@bp.patch("/<int:id>")
def update(id: int):
    data = BrandUpdateSchema().load(request.get_json() or {})
    b = Brand.query.get_or_404(id, description="Marca não encontrada")
    b.name = data["nome_marca"] # type: ignore
    db.session.commit()
    return jsonify({"id": b.id, "nome_marca": b.name})

@bp.delete("/<int:id>")
def remove(id: int):
    b = Brand.query.get_or_404(id, description="Marca não encontrada")
    db.session.delete(b)
    db.session.commit()
    return "", 204
