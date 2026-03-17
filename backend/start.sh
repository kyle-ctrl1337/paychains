#!/bin/bash
set -e

# Run database migrations
python -c "
from app.database import sync_engine, Base
import app.models
Base.metadata.create_all(sync_engine)
print('Database tables verified')
"

# Start Celery worker in background
celery -A app.workers.celery_app worker --loglevel=info --concurrency=2 &

# Start Celery beat in background
celery -A app.workers.celery_app beat --loglevel=info &

# Start FastAPI (foreground)
uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
