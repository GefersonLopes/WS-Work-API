import { Module } from '@nestjs/common';
import { TypeOrmModule, TypeOrmModuleOptions } from '@nestjs/typeorm';
import dataSource from '../../ormconfig';

@Module({
  imports: [
    TypeOrmModule.forRootAsync({
      useFactory: () => ({
        ...(dataSource.options as TypeOrmModuleOptions),
        autoLoadEntities: true,
        entities: undefined,
      }),
    }),
  ],
})
export class DatabaseModule {}
