from typing import Any, Dict, List, Tuple
from sqlalchemy import or_, text
from sqlalchemy.orm import joinedload
from werkzeug.exceptions import NotFound
from .models import Car, Fuel
from ..models.models import Model
from ..brands.models import Brand
from .schemas import CarCreateSchema, CarUpdateSchema
from ...extensions import db
from ...utils import escape_like

def _car_flat_json(c: Car) -> Dict[str, Any]:
    """Mesmo shape do NestJS (findAll): campos achatados."""
    return {
        "id": c.id,
        "timestamp_cadastro": c.createdAt.isoformat(),  # type: ignore
        "modelo_id": c.model_id,
        "ano": c.ano,
        "combustivel": c.combustivel.value,
        "num_portas": c.num_portas,
        "cor": c.cor,
        "nome_modelo": c.model.nome,
        "valor": float(c.model.fipeValue),
    }

def create_car(payload: dict) -> Dict[str, Any]:
    data = CarCreateSchema().load(payload)

    model = Model.query.get(data["modelo_id"]) # type: ignore
    if not model:
        raise NotFound("Modelo inválido")

    car = Car(
        model_id=model.id, # type: ignore
        ano=data["ano"], # type: ignore
        combustivel=Fuel[data["combustivel"]], # type: ignore
        num_portas=data["num_portas"], # type: ignore
        cor=data["cor"], # type: ignore
    )
    db.session.add(car)
    db.session.commit()

    car = Car.query.options(joinedload(Car.model)).get(car.id)  # type: ignore
    return _car_flat_json(car) # type: ignore

def list_cars(page: int, limit: int, search: str | None, model_id: int | None) -> Tuple[int, List[Dict[str, Any]]]:
    q = (
        Car.query.join(Model).join(Brand)
        .options(joinedload(Car.model).joinedload(Model.brand))
    )

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
    items = (
        q.order_by(Car.createdAt.desc())
         .offset((page - 1) * limit)
         .limit(limit)
         .all()
    )
    return total, [_car_flat_json(c) for c in items]

def get_car(id: int) -> Dict[str, Any]:
    c = (
        Car.query.options(joinedload(Car.model).joinedload(Model.brand))
        .get(id)
    )
    if not c:
        raise NotFound("Carro não encontrado")
    return _car_flat_json(c)

def update_car(id: int, payload: dict) -> Dict[str, Any]:
    data = CarUpdateSchema().load(payload, partial=True)

    car = Car.query.get(id)
    if not car:
        raise NotFound("Carro não encontrado")

    if "modelo_id" in data and data["modelo_id"] != car.model_id: # type: ignore
        m = Model.query.get(data["modelo_id"]) # type: ignore
        if not m:
            raise NotFound("Modelo inválido")
        car.model_id = m.id

    if "ano" in data: # type: ignore
        car.ano = data["ano"] # type: ignore
    if "combustivel" in data: # type: ignore
        car.combustivel = Fuel[data["combustivel"]] # type: ignore
    if "num_portas" in data: # type: ignore
        car.num_portas = data["num_portas"] # type: ignore
    if "cor" in data: # type: ignore
        car.cor = data["cor"] # type: ignore

    db.session.commit()

    car = Car.query.options(joinedload(Car.model)).get(car.id)  # type: ignore
    return _car_flat_json(car) # type: ignore

def remove_car(id: int) -> None:
    c = Car.query.get(id)
    if not c:
        raise NotFound("Carro não encontrado")
    db.session.delete(c)
    db.session.commit()
