import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { BrandsModule } from './modules/brands/brands.module';
import { ModelsModule } from './modules/models/models.module';
import { CarsModule } from './modules/cars/cars.module';

@Module({
  imports: [BrandsModule, ModelsModule, CarsModule],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}
