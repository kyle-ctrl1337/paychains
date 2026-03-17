#!/bin/bash
set -e

# Run database table creation (creates missing tables only)
python -c "
from app.database import sync_engine, Base
import app.models
Base.metadata.create_all(sync_engine)
print('Database tables verified')
"

# Start FastAPI (Celery worker & beat run as separate Railway services)
uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
