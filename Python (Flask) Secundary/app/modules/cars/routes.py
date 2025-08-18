from flask import Blueprint, request, jsonify
from ...common.dto import get_pagination_defaults
from .services import (
    create_car,
    list_cars,
    get_car,
    update_car,
    remove_car,
)

bp = Blueprint("cars", __name__)

@bp.post("/")
def create():
    payload = request.get_json() or {}
    result = create_car(payload)
    return jsonify(result), 201

@bp.get("/")
def list_all():
    page, limit, search = get_pagination_defaults()
    model_id = request.args.get("modelId", type=int)
    total, cars = list_cars(page, limit, search, model_id)
    return jsonify({"total": total, "page": page, "limit": limit, "cars": cars})

@bp.get("/<int:id>")
def find_one(id: int):
    result = get_car(id)
    return jsonify(result)

@bp.patch("/<int:id>")
def update(id: int):
    payload = request.get_json() or {}
    result = update_car(id, payload)
    return jsonify(result)

@bp.delete("/<int:id>")
def remove(id: int):
    remove_car(id)
    return "", 204
