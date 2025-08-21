import { Injectable, NotFoundException } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository, Brackets } from 'typeorm';
import { Car } from './entities/car.entity';
import { Model } from '../models/entities/model.entity';
import { CreateCarDto } from './dto/create-car.dto';
import { UpdateCarDto } from './dto/update-car.dto';
import { PaginationDto } from '../../common/dto/pagination.dto';

@Injectable()
export class CarsService {
  constructor(
    @InjectRepository(Car) private readonly repo: Repository<Car>,
    @InjectRepository(Model) private readonly models: Repository<Model>,
  ) {}

  async create(dto: CreateCarDto) {
    const model = await this.models.findOneBy({ id: dto.modelo_id });
    if (!model) throw new NotFoundException('Modelo inválido');
    const car = this.repo.create({
      model,
      ano: dto.ano,
      combustivel: dto.combustivel,
      num_portas: dto.num_portas,
      cor: dto.cor,
    });
    return this.repo.save(car);
  }

  private escapeLike(input: string) {
    return input.replace(/[%_]/g, (m) => '\\' + m);
  }

  async findAll(q: PaginationDto & { modelId?: number }) {
    const page = Math.max(1, Number(q.page || 1));
    const limit = Math.min(100, Math.max(1, Number(q.limit || 20)));
    const offset = (page - 1) * limit;

    const qb = this.repo
      .createQueryBuilder('car')
      .leftJoinAndSelect('car.model', 'model')
      .leftJoinAndSelect('model.brand', 'brand')
      .orderBy('car.createdAt', 'DESC')
      .take(limit)
      .skip(offset);

    if (q.modelId) {
      qb.andWhere('model.id = :modelId', { modelId: q.modelId });
    }

    if (q.search && String(q.search).trim().length > 0) {
      const raw = String(q.search).trim();
      const like = `%${this.escapeLike(raw)}%`;
      const maybeNumber = Number(raw);
      const isNumeric = !Number.isNaN(maybeNumber);

      qb.andWhere(
        new Brackets((w) => {
          w.where("car.cor ILIKE :like ESCAPE '\\'", { like })
            .orWhere("car.combustivel ILIKE :like ESCAPE '\\'", { like })
            .orWhere("model.nome ILIKE :like ESCAPE '\\'", { like })
            .orWhere("brand.nome_marca ILIKE :like ESCAPE '\\'", { like });

          if (isNumeric) {
            w.orWhere('car.ano = :n', { n: maybeNumber }).orWhere(
              'car.num_portas = :n',
              { n: maybeNumber },
            );
          }
        }),
      );
    }

    const [items, total] = await qb.getManyAndCount();

    const cars = items.map((car) => ({
      id: car.id,
      timestamp_cadastro: car.createdAt,
      modelo_id: car.model.id,
      ano: car.ano,
      combustivel: car.combustivel,
      num_portas: car.num_portas,
      cor: car.cor,
      nome_modelo: car.model.nome,
      nome_marca: car.model.brand.name,
      valor: car.model.fipeValue,
    }));

    return { total, page, limit, cars };
  }

  async findOne(id: number) {
    const c = await this.repo.findOne({
      where: { id },
      relations: { model: { brand: true } },
    });
    if (!c) throw new NotFoundException('Carro não encontrado');
    return c;
  }

  private assignDefined<T>(target: T, patch: Partial<T>) {
    for (const [k, v] of Object.entries(patch)) {
      // eslint-disable-next-line @typescript-eslint/no-unsafe-member-access
      if (v !== undefined) (target as any)[k] = v;
    }
  }

  async update(id: number, dto: UpdateCarDto) {
    const car = await this.findOne(id);

    if (dto.modelo_id && dto.modelo_id !== car.model.id) {
      const model = await this.models.findOneBy({ id: dto.modelo_id });
      if (!model) throw new NotFoundException('Modelo inválido');
      car.model = model;
    }

    const patch = {
      ano: dto.ano,
      combustivel: dto.combustivel,
      num_portas: dto.num_portas,
      cor: dto.cor,
    };

    this.assignDefined(car, patch);

    return this.repo.save(car);
  }

  async remove(id: number) {
    const c = await this.findOne(id);
    await this.repo.remove(c);
  }
}
