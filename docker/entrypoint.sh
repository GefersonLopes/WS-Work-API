#!/usr/bin/env sh
set -e

DB_HOST="${DB_HOST:-db}"
DB_PORT="${DB_PORT:-5432}"

echo "Aguardando banco em ${DB_HOST}:${DB_PORT} ..."
until nc -z "${DB_HOST}" "${DB_PORT}"; do
  sleep 0.5
done

echo "Executando migrations (TypeORM + ts-node, usando seu ormconfig.ts)..."
export TS_NODE_TRANSPILE_ONLY=1
node -r ts-node/register ./node_modules/typeorm/cli.js migration:run -d ormconfig.ts

if [ "${RUN_SEED}" = "true" ]; then
  echo "Executando seed..."
  node -r ts-node/register src/database/seed/seed.ts || echo "Seed falhou (ok, continuando)"
else
  echo "RUN_SEED != true — pulando seed."
fi

echo "Iniciando API..."
export NODE_PATH=/app/dist
node -e "require('module').Module._initPaths(); require('./dist/src/main.js');"
