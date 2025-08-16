import {
  Column,
  Entity,
  ManyToOne,
  OneToMany,
  PrimaryGeneratedColumn,
  Unique,
  Index,
  JoinColumn,
  RelationId,
} from 'typeorm';
import { Brand } from '../../brands/entities/brand.entity';
import { Car } from '../../cars/entities/car.entity';
import { DecimalTransformer } from '../../../common/utils/decimal.transformer';

@Entity('models')
@Unique(['nome', 'brand'])
export class Model {
  @PrimaryGeneratedColumn('increment')
  id: number;

  @Index()
  @ManyToOne(() => Brand, (b) => b.models, {
    nullable: false,
    onDelete: 'RESTRICT',
  })
  @JoinColumn({ name: 'marca_id' })
  brand: Brand;

  @RelationId((m: Model) => m.brand)
  brandId: number;

  @Column({ name: 'nome', type: 'varchar', length: 120 })
  nome: string;

  @Column({
    name: 'valor_fipe',
    type: 'decimal',
    precision: 12,
    scale: 2,
    transformer: DecimalTransformer,
  })
  fipeValue: number;

  @OneToMany(() => Car, (c) => c.model, { cascade: false })
  cars: Car[];
}
