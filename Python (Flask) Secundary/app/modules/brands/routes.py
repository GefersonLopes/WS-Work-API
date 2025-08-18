from flask import Blueprint, request, jsonify
from ...extensions import db
from . import services as services

bp = Blueprint("brands", __name__)

@bp.post("/")
def create():
    payload = request.get_json() or {}
    result = services.create(payload)
    return jsonify(result), 201
    
    

@bp.get("/")
def list_all():
    result = services.list_all()
    return jsonify(result)
    

@bp.get("/<int:id>")
def find_one(id: int):
    result = services.find_one(id)
    return jsonify(result)
    

@bp.patch("/<int:id>")
def update(id: int):
    payload = request.get_json() or {}
    result = services.update(id, payload)
    return jsonify(result)
    

@bp.delete("/<int:id>")
def remove(id: int):
    services.remove(id)
    return "", 204
    
