import {
  Column,
  Entity,
  OneToMany,
  PrimaryGeneratedColumn,
  Unique,
} from 'typeorm';
import { Model } from '../../models/entities/model.entity';

@Entity('brands')
@Unique(['name'])
export class Brand {
  @PrimaryGeneratedColumn('increment')
  id: number;

  @Column({ name: 'nome_marca', type: 'varchar', length: 120 })
  name: string;

  @OneToMany(() => Model, (m) => m.brand, { cascade: false })
  models: Model[];
}
