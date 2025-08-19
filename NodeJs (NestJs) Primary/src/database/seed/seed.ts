import dataSource from '../../../ormconfig';
import { Brand } from '../../modules/brands/entities/brand.entity';
import { Model } from '../../modules/models/entities/model.entity';
import { Car, Fuel } from '../../modules/cars/entities/car.entity';
import { input } from './data.seed';

export type InputCar = {
  id: number;
  timestamp_cadastro: number;
  modelo_id: number;
  ano: number;
  combustivel: keyof typeof Fuel;
  num_portas: number;
  cor: string;
  nome_modelo: string;
  valor: string | number;
};

function guessBrandName(modelName: string): string {
  const n = modelName.toUpperCase();

  if (/(SW4|HILUX|GR COROLLA|COROLLA)/.test(n)) return 'Toyota';

  if (/(RS6|AUDI)/.test(n)) return 'Audi';

  if (/(RANGE ROVER|DEFENDER)/.test(n)) return 'Land Rover';

  if (/\bSEAL\b/.test(n)) return 'BYD';

  if (/(911|MACAN|PANAMERA|CAYENNE)/.test(n)) return 'Porsche';

  if (/(^|\s)1500\sREBEL/.test(n)) return 'RAM';

  if (/(MUSTANG|RANGER RAPTOR)/.test(n)) return 'Ford';

  if (/CIVIC/.test(n)) return 'Honda';

  if (/(^|\s)I4\b|M2 COMPETITION|X6 M/.test(n)) return 'BMW';

  return 'Marca Desconhecida';
}

function parseValor(v: string | number): number {
  if (typeof v === 'number') return v;
  const cleaned = v.replace(/\./g, '').replace(',', '.');
  const num = Number(cleaned);
  if (Number.isNaN(num)) throw new Error(`Valor inválido: ${v}`);
  return num;
}

function epochToDate(ts: number): Date {
  const n = Number(ts);
  const len = String(Math.trunc(Math.abs(n))).length;
  if (len >= 13) return new Date(n);
  if (len <= 10) return new Date(n * 1000);
  return new Date(n > 2_000_000_000 ? n : n * 1000);
}

async function run() {
  await dataSource.initialize();

  const brandRepo = dataSource.getRepository(Brand);
  const modelRepo = dataSource.getRepository(Model);
  const carRepo = dataSource.getRepository(Car);

  const brandByName = new Map<string, Brand>();
  const modelById = new Map<number, Model>();

  for (const c of input.cars) {
    const brandName = guessBrandName(c.nome_modelo);
    let brand =
      brandByName.get(brandName) ??
      (await brandRepo.findOne({ where: { name: brandName } }));

    if (!brand) {
      brand = brandRepo.create({ name: brandName });
      await brandRepo.save(brand);
      brandByName.set(brandName, brand);
    }

    if (!modelById.has(c.modelo_id)) {
      let model = await modelRepo.findOne({
        where: { id: Number(c.modelo_id) },
      });

      if (!model) {
        model = modelRepo.create({
          id: c.modelo_id,
          nome: c.nome_modelo,
          fipeValue: parseValor(c.valor),
          brand,
        });
        await modelRepo.save(model);
      }

      modelById.set(c.modelo_id, model);
    }
  }

  for (const c of input.cars) {
    const model = modelById.get(c.modelo_id)!;

    const car = carRepo.create({
      id: c.id,
      createdAt: epochToDate(c.timestamp_cadastro),
      model,
      ano: c.ano,
      combustivel: c.combustivel.toUpperCase() as Fuel,
      num_portas: c.num_portas,
      cor: c.cor,
    });

    await carRepo.save(car);
  }

  console.log('Seed concluído com sucesso.');
  await dataSource.destroy();
}

run().catch((e) => {
  console.error(e);
  process.exit(1);
});
