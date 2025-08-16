from ..extensions import db
from ..modules.brands.models import Brand
from ..modules.models.models import Model
from ..modules.cars.models import Car, Fuel
from ..utils import normalize_upper_no_accent
from datetime import datetime

def epoch_to_dt(ts: int) -> datetime:
    s = int(ts)
    digits = len(str(abs(s)))
    if digits >= 13: return datetime.fromtimestamp(s/1000)
    return datetime.fromtimestamp(s)

def parse_valor(v):
    if isinstance(v,(int,float)): return float(v)
    return float(v.replace(".","").replace(",", "."))

input_data = {
  "cars":[
    {"id":1,"timestamp_cadastro":1696539488,"modelo_id":12,"ano":2015,"combustivel":"FLEX","num_portas":4,"cor":"BEGE","nome_modelo":"ONIX PLUS","valor":"50.000"},
    {"id":2,"timestamp_cadastro":1696531234,"modelo_id":14,"ano":2014,"combustivel":"FLEX","num_portas":4,"cor":"AZUL","nome_modelo":"JETTA","valor":"49.000"},
    {"id":3,"timestamp_cadastro":16965354321,"modelo_id":79,"ano":1993,"combustivel":"DIESEL","num_portas":4,"cor":"AZUL","nome_modelo":"HILUX SW4","valor":"47.500"}
  ]
}

def guess_brand(model_name: str) -> str:
    n = model_name.upper()
    if "ONIX" in n: return "Chevrolet"
    if "JETTA" in n: return "Volkswagen"
    if "HILUX" in n: return "Toyota"
    return "Marca Desconhecida"

def run_seed():
    brand_by_name = {}
    model_by_id = {}

    for c in input_data["cars"]:
        bname = guess_brand(c["nome_modelo"])
        brand = brand_by_name.get(bname) or Brand.query.filter_by(name=bname).first()
        if not brand:
            brand = Brand(name=bname)
            db.session.add(brand); db.session.flush()
            brand_by_name[bname] = brand

        if c["modelo_id"] not in model_by_id:
            model = Model.query.get(c["modelo_id"])
            if not model:
                model = Model(id=c["modelo_id"], nome=c["nome_modelo"], fipeValue=parse_valor(c["valor"]), brand_id=brand.id)
                db.session.add(model); db.session.flush()
            model_by_id[c["modelo_id"]] = model

    for c in input_data["cars"]:
        model = model_by_id[c["modelo_id"]]
        car = Car.query.get(c["id"])
        if not car:
            car = Car(id=c["id"],
                      createdAt=epoch_to_dt(c["timestamp_cadastro"]),
                      model_id=model.id,
                      ano=c["ano"],
                      combustivel=Fuel[normalize_upper_no_accent(c["combustivel"])],
                      num_portas=c["num_portas"],
                      cor=c["cor"])
            db.session.add(car)
    db.session.commit()
    print("Seed concluído com sucesso.")
