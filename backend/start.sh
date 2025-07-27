#!/bin/bash

# Exit on error
set -e

# Run migrations
echo "🔄 Running Alembic migrations..."
alembic upgrade head

if [[ "$AUTO_SEED" == "true" ]]; then
  echo "🌱 Running database seeder..."
  python app/db/seed.py || echo "⚠️ Seeder failed or already ran"
fi

# Start the FastAPI app
echo "🚀 Starting FastAPI..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
