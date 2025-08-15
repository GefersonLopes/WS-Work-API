import { Injectable, NotFoundException } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository, ILike } from 'typeorm';
import { Model } from './entities/model.entity';
import { Brand } from '../brands/entities/brand.entity';
import { CreateModelDto } from './dto/create-model.dto';
import { UpdateModelDto } from './dto/update-model.dto';
import { PaginationDto } from '../../common/dto/pagination.dto';

@Injectable()
export class ModelsService {
  constructor(
    @InjectRepository(Model) private readonly repo: Repository<Model>,
    @InjectRepository(Brand) private readonly brands: Repository<Brand>,
  ) {}

  async create(dto: CreateModelDto) {
    const brand = await this.brands.findOneBy({ id: dto.marca_id });
    if (!brand) throw new NotFoundException('Marca inválida');
    const model = this.repo.create({
      brand,
      nome: dto.nome,
      fipeValue: dto.fipeValue,
    });
    return this.repo.save(model);
  }

  async findAll(p: PaginationDto) {
    const [items, total] = await this.repo.findAndCount({
      relations: { brand: true },
      where: p.search ? { nome: ILike(`%${p.search}%`) } : {},
      order: { nome: 'ASC' },
      skip: (p.page - 1) * p.limit,
      take: p.limit,
    });
    return { total, page: p.page, limit: p.limit, items };
  }

  async findOne(id: number) {
    const m = await this.repo.findOne({
      where: { id },
      relations: { brand: true },
    });
    if (!m) throw new NotFoundException('Modelo não encontrado');
    return m;
  }

  async update(id: number, dto: UpdateModelDto) {
    const m = await this.findOne(id);
    if (dto.marca_id && dto.marca_id !== m.brand.id) {
      const brand = await this.brands.findOneBy({ id: dto.marca_id });
      if (!brand) throw new NotFoundException('Marca inválida');
      m.brand = brand;
    }
    m.nome = dto.nome ?? m.nome;
    m.fipeValue = dto.fipeValue ?? m.fipeValue;
    return this.repo.save(m);
  }

  async remove(id: number) {
    const m = await this.findOne(id);
    await this.repo.remove(m);
  }
}
