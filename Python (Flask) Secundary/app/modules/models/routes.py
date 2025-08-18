from flask import Blueprint, request, jsonify
from ...common.dto import get_pagination_defaults
from .services import (
    create_model,
    list_models,
    get_model,
    update_model,
    remove_model,
)

bp = Blueprint("models", __name__)

@bp.post("/")
def create():
    payload = request.get_json() or {}
    result = create_model(payload)
    return jsonify(result), 201

@bp.get("/")
def list_all():
    page, limit, search = get_pagination_defaults()
    total, items = list_models(page, limit, search)
    return jsonify({"total": total, "page": page, "limit": limit, "items": items})

@bp.get("/<int:id>")
def find_one(id: int):
    result = get_model(id)
    return jsonify(result)

@bp.patch("/<int:id>")
def update(id: int):
    payload = request.get_json() or {}
    result = update_model(id, payload)
    return jsonify(result)

@bp.delete("/<int:id>")
def remove(id: int):
    remove_model(id)
    return "", 204
