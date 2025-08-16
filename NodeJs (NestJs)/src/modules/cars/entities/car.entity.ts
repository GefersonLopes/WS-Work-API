import {
  Column,
  CreateDateColumn,
  Entity,
  ManyToOne,
  PrimaryGeneratedColumn,
  Check,
  Index,
  JoinColumn,
  RelationId,
} from 'typeorm';
import { Model } from '../../models/entities/model.entity';

export enum Fuel {
  GASOLINA = 'GASOLINA',
  ETANOL = 'ETANOL',
  FLEX = 'FLEX',
  DIESEL = 'DIESEL',
  HIBRIDO = 'HIBRIDO',
  ELETRICO = 'ELETRICO',
}

@Entity('cars')
@Check(`"num_portas" BETWEEN 2 AND 6`)
@Check(`"ano" BETWEEN 1950 AND EXTRACT(YEAR FROM now())::int + 1`)
export class Car {
  @PrimaryGeneratedColumn('increment')
  id: number;

  @CreateDateColumn({ name: 'timestamp_cadastro' })
  createdAt: Date;

  @ManyToOne(() => Model, (m) => m.cars, {
    nullable: false,
    onDelete: 'RESTRICT',
  })
  @JoinColumn({ name: 'modelo_id' })
  @Index('IDX_car_model')
  model: Model;

  @RelationId((c: Car) => c.model)
  modelId: number;

  @Column({ type: 'int' })
  ano: number;

  @Column({ type: 'enum', enum: Fuel })
  combustivel: Fuel;

  @Column({ name: 'num_portas', type: 'int' })
  num_portas: number;

  @Column({ type: 'varchar', length: 40 })
  cor: string;
}
