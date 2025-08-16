import { Injectable, NotFoundException } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { Brand } from './entities/brand.entity';
import { CreateBrandDto } from './dto/create-brand.dto';
import { UpdateBrandDto } from './dto/update-brand.dto';

@Injectable()
export class BrandsService {
  constructor(
    @InjectRepository(Brand) private readonly repo: Repository<Brand>,
  ) {}

  async create(dto: CreateBrandDto) {
    const brand = this.repo.create({ name: dto.nome_marca });
    return this.repo.save(brand);
  }

  findAll() {
    return this.repo.find({ order: { name: 'ASC' } });
  }

  async findOne(id: number) {
    const b = await this.repo.findOne({ where: { id } });
    if (!b) throw new NotFoundException('Marca não encontrada');
    return b;
  }

  async update(id: number, dto: UpdateBrandDto) {
    const b = await this.findOne(id);
    if (!dto.nome_marca)
      throw new NotFoundException('Nome da marca é obrigatório');
    b.name = dto.nome_marca;
    return this.repo.save(b);
  }

  async remove(id: number) {
    const b = await this.findOne(id);
    await this.repo.remove(b);
  }
}
