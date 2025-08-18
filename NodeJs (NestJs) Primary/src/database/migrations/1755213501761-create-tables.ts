import {
  MigrationInterface,
  QueryRunner,
  Table,
  TableForeignKey,
  TableUnique,
  TableIndex,
  TableCheck,
} from 'typeorm';

export class CreateTables1755213501761 implements MigrationInterface {
  public async up(queryRunner: QueryRunner): Promise<void> {
    await queryRunner.createTable(
      new Table({
        name: 'brands',
        columns: [
          {
            name: 'id',
            type: 'int',
            isPrimary: true,
            isGenerated: true,
            generationStrategy: 'increment',
          },
          {
            name: 'nome_marca',
            type: 'varchar',
            length: '120',
            isNullable: false,
          },
        ],
        uniques: [
          new TableUnique({
            columnNames: ['nome_marca'],
            name: 'UQ_brand_nome',
          }),
        ],
      }),
    );

    await queryRunner.createTable(
      new Table({
        name: 'models',
        columns: [
          {
            name: 'id',
            type: 'int',
            isPrimary: true,
            isGenerated: true,
            generationStrategy: 'increment',
          },
          { name: 'marca_id', type: 'int', isNullable: false },
          { name: 'nome', type: 'varchar', length: '120', isNullable: false },
          {
            name: 'valor_fipe',
            type: 'decimal',
            precision: 12,
            scale: 2,
            isNullable: false,
          },
        ],
        uniques: [
          new TableUnique({
            columnNames: ['nome', 'marca_id'],
            name: 'UQ_model_nome_brand',
          }),
        ],
        indices: [
          new TableIndex({
            columnNames: ['marca_id'],
            name: 'IDX_model_brand',
          }),
        ],
        foreignKeys: [
          new TableForeignKey({
            columnNames: ['marca_id'],
            referencedTableName: 'brands',
            referencedColumnNames: ['id'],
            onDelete: 'CASCADE',
          }),
        ],
      }),
    );

    await queryRunner.createTable(
      new Table({
        name: 'cars',
        columns: [
          {
            name: 'id',
            type: 'int',
            isPrimary: true,
            isGenerated: true,
            generationStrategy: 'increment',
          },
          {
            name: 'timestamp_cadastro',
            type: 'timestamptz',
            isNullable: false,
            default: 'now()',
          },
          { name: 'modelo_id', type: 'int', isNullable: false },
          { name: 'ano', type: 'int', isNullable: false },
          {
            name: 'combustivel',
            type: 'varchar',
            length: '10',
            isNullable: false,
          },
          { name: 'num_portas', type: 'int', isNullable: false },
          { name: 'cor', type: 'varchar', length: '40', isNullable: false },
        ],
        foreignKeys: [
          new TableForeignKey({
            columnNames: ['modelo_id'],
            referencedTableName: 'models',
            referencedColumnNames: ['id'],
            onDelete: 'CASCADE',
          }),
        ],
        indices: [
          new TableIndex({ columnNames: ['modelo_id'], name: 'IDX_car_model' }),
          new TableIndex({
            columnNames: ['timestamp_cadastro'],
            name: 'IDX_car_createdAt',
          }),
        ],
        checks: [
          new TableCheck({
            name: 'CHK_car_num_portas',
            expression: `"num_portas" BETWEEN 2 AND 6`,
          }),
          new TableCheck({
            name: 'CHK_car_ano',
            expression: `"ano" BETWEEN 1950 AND 2100`,
          }),
          new TableCheck({
            name: 'CHK_car_combustivel',
            expression: `"combustivel" IN ('GASOLINA','ETANOL','FLEX','DIESEL','HIBRIDO','ELETRICO')`,
          }),
        ],
      }),
    );
  }

  public async down(queryRunner: QueryRunner): Promise<void> {
    await queryRunner.dropTable('cars');
    await queryRunner.dropTable('models');
    await queryRunner.dropTable('brands');
  }
}
