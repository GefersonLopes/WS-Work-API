import { Injectable, NotFoundException } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository, ILike } from 'typeorm';
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

  async findAll(q: PaginationDto & { modelId?: number }) {
    const where = {} as { [key: string]: any };
    if (q.search) where.cor = ILike(`%${q.search}%`);
    if (q['modelId']) where.model = { id: q['modelId'] };

    const [items, total] = await this.repo.findAndCount({
      relations: { model: { brand: true } },
      where,
      order: { createdAt: 'DESC' },
      take: q.limit,
      skip: (q.page - 1) * q.limit,
    });

    const cars = items.map((car) => ({
      id: car.id,
      timestamp_cadastro: car.createdAt,
      modelo_id: car.model.id,
      ano: car.ano,
      combustivel: car.combustivel,
      num_portas: car.num_portas,
      cor: car.cor,
      nome_modelo: car.model.nome,
      valor: car.model.fipeValue,
    }));

    return { total, page: q.page, limit: q.limit, cars };
  }

  async findOne(id: number) {
    const c = await this.repo.findOne({
      where: { id },
      relations: { model: { brand: true } },
    });
    if (!c) throw new NotFoundException('Carro não encontrado');
    return c;
  }

  async update(id: number, dto: UpdateCarDto) {
    const car = await this.findOne(id);
    if (dto.modelo_id && dto.modelo_id !== car.model.id) {
      const model = await this.models.findOneBy({ id: dto.modelo_id });
      if (!model) throw new NotFoundException('Modelo inválido');
      car.model = model;
    }
    Object.assign(car, {
      ano: dto.ano,
      combustivel: dto.combustivel,
      num_portas: dto.num_portas,
      cor: dto.cor,
    });
    return this.repo.save(car);
  }

  async remove(id: number) {
    const c = await this.findOne(id);
    await this.repo.remove(c);
  }
}
