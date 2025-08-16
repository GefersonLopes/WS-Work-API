import {
  IsEnum,
  IsInt,
  IsNotEmpty,
  IsString,
  Max,
  IsNumber,
  Min,
  MaxLength,
} from 'class-validator';
import { Type } from 'class-transformer';
import { Fuel } from '../entities/car.entity';

export class CreateCarDto {
  @IsNumber() modelo_id: number;

  @Type(() => Number)
  @IsInt()
  @Min(1950)
  @Max(new Date().getFullYear() + 1)
  ano: number;

  @IsEnum(Fuel) combustivel: Fuel;

  @Type(() => Number)
  @IsInt()
  @Min(2)
  @Max(6)
  num_portas: number;

  @IsString()
  @IsNotEmpty()
  @MaxLength(40)
  cor: string;
}
