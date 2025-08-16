from flask import Blueprint, request, jsonify
from sqlalchemy import or_, and_, text
from .models import Car, Fuel
from ..models.models import Model
from ..brands.models import Brand
from .schemas import CarCreateSchema, CarUpdateSchema
from ...extensions import db
from ...common.dto import get_pagination_defaults
from ...utils import escape_like

bp = Blueprint("cars", __name__)

@bp.post("/")
def create():
    data = CarCreateSchema().load(request.get_json() or {})
    model = Model.query.get(data["modelo_id"]) # type: ignore
    if not model: return jsonify({"message":"Modelo inválido"}), 404
    car = Car(model_id=model.id, ano=data["ano"], combustivel=Fuel[data["combustivel"]], # type: ignore
              num_portas=data["num_portas"], cor=data["cor"]) # type: ignore
    db.session.add(car); db.session.commit()
    
    return jsonify({
        "id": car.id,
        "ano": car.ano,
        "combustivel": car.combustivel.name,
        "num_portas": car.num_portas,
        "cor": car.cor,
        "createdAt": car.createdAt if car.createdAt else None,
        "modelo": {
            "id": model.id,
            "nome": model.nome,
            "fipeValue": float(model.fipeValue),
            "brand": {
                "id": model.brand.id,
                "nome": model.brand.name
            }
        }
    }), 201

@bp.get("/")
def list_all():
    page, limit, search = get_pagination_defaults()
    model_id = request.args.get("modelId", type=int)

    q = Car.query.join(Model).join(Brand)\
        .options(db.joinedload(Car.model).joinedload(Model.brand))

    if model_id:
        q = q.filter(Car.model_id == model_id)

    if search:
        like = f"%{escape_like(search)}%"
        is_num = search.isdigit()
        clauses = [
            Car.cor.ilike(like, escape='\\'),
            text("CAST(cars.combustivel AS TEXT) ILIKE :like ESCAPE '\\'"),
            Model.nome.ilike(like, escape='\\'),
            Brand.name.ilike(like, escape='\\'),
        ]
        params = {"like": like}
        if is_num:
            n = int(search)
            clauses += [Car.ano == n, Car.num_portas == n]
        q = q.filter(or_(*clauses)).params(**params)

    total = q.count()
    items = q.order_by(Car.createdAt.desc()).offset((page-1)*limit).limit(limit).all()

    cars = [{
        "id": c.id,
        "timestamp_cadastro": c.createdAt.isoformat(),
        "modelo_id": c.model_id,
        "ano": c.ano,
        "combustivel": c.combustivel.value,
        "num_portas": c.num_portas,
        "cor": c.cor,
        "nome_modelo": c.model.nome,
        "valor": float(c.model.fipeValue),
    } for c in items]

    return jsonify({"total": total, "page": page, "limit": limit, "cars": cars})

@bp.get("/<int:id>")
def find_one(id: int):
    c = Car.query.options(db.joinedload(Car.model).joinedload(Model.brand)).get_or_404(id, description="Carro não encontrado")
    return jsonify({
        "id": c.id,
        "timestamp_cadastro": c.createdAt.isoformat(),
        "modelo_id": c.model_id,
        "ano": c.ano,
        "combustivel": c.combustivel.value,
        "num_portas": c.num_portas,
        "cor": c.cor,
        "nome_modelo": c.model.nome,
        "valor": float(c.model.fipeValue),
    })

@bp.patch("/<int:id>")
def update(id: int):
    data = CarUpdateSchema().load(request.get_json() or {})
    car = Car.query.get_or_404(id, description="Carro não encontrado")

    if "modelo_id" in data and data["modelo_id"] != car.model_id: # type: ignore
        m = Model.query.get(data["modelo_id"]) # type: ignore
        if not m: return jsonify({"message":"Modelo inválido"}), 404
        car.model_id = m.id
    if "ano" in data: car.ano = data["ano"] # type: ignore
    if "combustivel" in data: car.combustivel = Fuel[data["combustivel"]] # type: ignore
    if "num_portas" in data: car.num_portas = data["num_portas"] # type: ignore
    if "cor" in data: car.cor = data["cor"] # type: ignore

    db.session.commit()
    return jsonify({
        "id": car.id,
        "ano": car.ano,
        "combustivel": car.combustivel.name,
        "num_portas": car.num_portas,
        "cor": car.cor,
        "createdAt": car.createdAt if car.createdAt else None,
    })

@bp.delete("/<int:id>")
def remove(id: int):
    c = Car.query.get_or_404(id, description="Carro não encontrado")
    db.session.delete(c); db.session.commit()
    return "", 204
