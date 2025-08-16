#!/usr/bin/env sh
set -e

DB_HOST="${DB_HOST:-db}"
DB_PORT="${DB_PORT:-5432}"

echo "Aguardando Postgres em $DB_HOST:$DB_PORT ..."
until nc -z "$DB_HOST" "$DB_PORT"; do
  sleep 0.5
done

echo "DEBUG: conferindo driver e URI..."
python - <<'PY'
import os
from app.config import Config
print("  DATABASE_URL:", os.getenv("DATABASE_URL"))
print("  SQLALCHEMY_DATABASE_URI:", Config.SQLALCHEMY_DATABASE_URI)
# Testa import do pg8000
import pg8000
print("  pg8000 OK:", pg8000.__version__)
PY

echo "Aplicando migrations..."
export FLASK_APP="${FLASK_APP:-wsgi.py}"
flask db upgrade

if [ "${RUN_SEED}" = "true" ]; then
  echo "Rodando seed..."
  python - <<'PY'
from app import create_app
from app.database.seed import run_seed
app = create_app()
with app.app_context():
    run_seed()
PY
else
  echo "RUN_SEED != true — pulando seed."
fi

echo "Subindo API com gunicorn..."
exec gunicorn -w 4 -b 0.0.0.0:${PORT:-3000} wsgi:app
