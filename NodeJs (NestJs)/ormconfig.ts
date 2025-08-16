import 'dotenv/config';
import { DataSource } from 'typeorm';
import { join } from 'path';

export default new DataSource({
  type: 'postgres',
  host: process.env.DB_HOST,
  port: +(process.env.DB_PORT || 5432),
  username: process.env.DB_USER,
  password: process.env.DB_PASS,
  database: process.env.DB_NAME,
  entities: [join(__dirname, 'src', 'modules', '**', '*.entity.{ts,js}')],
  migrations: [join(__dirname, 'src', 'database', 'migrations', '*.{ts,js}')],
  synchronize: false,
  logging: false,
  migrationsRun: true,
});
