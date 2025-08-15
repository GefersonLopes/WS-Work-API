import {
  IsNotEmpty,
  IsString,
  IsNumber,
  Min,
  MaxLength,
} from 'class-validator';

export class CreateModelDto {
  @IsNumber() marca_id: number;
  @IsString() @IsNotEmpty() @MaxLength(120) nome: string;
  @IsNumber() @Min(0) fipeValue: number;
}
